import pandas as pd
from algorithms.repair import Repair
from algorithms.dependency_graph import DependencyGraph
from statistics import median
from collections import Counter


class OFDClean(object):

    def __init__(self, data, ofds, senses, right_attrs, ssets, threshold):
        """
        data(DataFrame): data to be cleaned
        ofds(array): OFDs ([[left attributes], right attribute])
        ssets(dictionary): right values->senses
        senses(dictionary): sense(values of ssets)->synonym values
        """
        self.threshold = threshold

        self.data = data
        self.ofds = ofds
        self.senses = senses
        self.right_attrs = right_attrs
        self.ssets = ssets

        self.eqTupleNumList = []  # [{key: left attributes string, value: related tuple nums} for each ofd]
        self.overlapMap = {}  # reversed hashmap of eqTupleNumList, for building dependency graph
        self.eqTupleMap = {}  # {key: left attributes string, value: related tuple right values}
        self.eqRightAttrMap = {}  # {key: left attributes string, value: related tuple right column name}
        self.getEquivalenceClass()
        # print('eqTupleNumList:\n', self.eqTupleNumList)
        # print('overlapMap:\n', self.overlapMap)
        print('\n==========OFDClean Initialized==========\n')

    def getEquivalenceClass(self):
        for index, row in self.ofds.iterrows():
            left_attrs = row['left'].split(',')
            right_attr = row['right']
            # print('left_attrs:', left_attrs)
            # print('right_attr:', right_attr)
            left_attrs.append(right_attr)
            selected_columns = self.data[left_attrs]
            # print('selected_columns:\n', selected_columns)

            eqTupleNumMap = {}
            for index, row in selected_columns.iterrows():
                left_vals = row[:-1].tolist()
                left_vals = ','.join([str(elem) for elem in left_vals])
                # print('left_vals:', left_vals)
                # right_val = row[-1]
                # print('right_val:', right_val)
                if left_vals in eqTupleNumMap:
                    eqTupleNumMap[left_vals] += [index]
                else:
                    eqTupleNumMap[left_vals] = [index]
                
                if index in self.overlapMap:
                    self.overlapMap[index] += [left_vals]
                else:
                    self.overlapMap[index] = [left_vals]

            self.eqTupleNumList.append(eqTupleNumMap)

    def run(self):
        self.init_assign()
        print('\n==========Initial Sense Assignment==========')
        print(self.eqSenseList)

        print('\n==========Dependency Graph==========')
        DG = DependencyGraph(self.eqTupleNumList, self.eqSenseList, self.senses, self.overlapMap, self.eqTupleMap, self.eqRightAttrMap, self.threshold)
        DG.display()

        print('\n==========Refined Sense Assignment==========')
        DG.BFS('local')
        print(DG.refined_eqSenseMap)

        print('\n==========Optimal Sense Assignment==========')
        DG.BFS('optimal')
        print(DG.optimal_eqSenseMap)

        from utils import statistics
        statistics(DG.refined_eqSenseMap, DG.eqSenseMap)
        statistics(DG.refined_eqSenseMap, DG.optimal_eqSenseMap)

        # self.Repair = Repair(DG.refined_eqSenseMap, self.eqTupleMap, self.senses)
        # self.Repair.identifyErrors()
        # print('ontologyCandidate:\n', self.Repair.ontologyCandidates)
        # print('nodeSenseMap:\n', self.Repair.nodeSenseMap)
        # self.Repair.beam_search()
        # print('solutionMap:\n', self.Repair.solutionMap)

    # assign a local optimal sense for each equivalence class
    def init_assign(self):
        self.eqSenseList = []

        # for each ofd
        for ofd_right_attr, eqTupleNumMap in zip(self.right_attrs, self.eqTupleNumList):
            eqSenseMap = dict.fromkeys(eqTupleNumMap.keys())

            # for each equivalence class
            for left_vals, eqTupleNums in eqTupleNumMap.items():
                # print('left_vals:', left_vals)
                right_vals = [self.data.iloc[tuple_num, self.data.columns.get_loc(ofd_right_attr)] for tuple_num in eqTupleNums]
                # print('right values:\n', right_vals)
                self.eqTupleMap[left_vals] = right_vals
                self.eqRightAttrMap[left_vals] = ofd_right_attr
                freq = dict(Counter(right_vals))
                # print('freq:', freq)

                # k = stats.median_absolute_deviation(list(freq.values()))
                # MAD = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

                # sort right values by deviation from median frequency
                median_freq = median(freq.values())
                deviation = {k: abs(v - median_freq) for k, v in freq.items()}  # key: right values, value: list of senses of right values
                deviation = dict(sorted(deviation.items(), key=lambda item: item[1], reverse=False))  # sort in ascending order
                # print('deviation:', deviation)
                k = len(deviation)
                # print('k =', k)

                sorted_senses = []
                sorted_right_vals = list(deviation.keys())
                for v in sorted_right_vals:
                    # print('value:', v)
                    # print('ssets[ofd_right_attr].keys():', self.ssets[ofd_right_attr].keys())
                    if v in self.ssets[ofd_right_attr].keys():
                        # print('ssets[ofd_right_attr][v]:', self.ssets[ofd_right_attr][v])
                        if self.ssets[ofd_right_attr][v] not in sorted_senses:
                            sorted_senses.append(self.ssets[ofd_right_attr][v])
                # print('sorted_right_vals', sorted_right_vals)
                # print('sorted_senses', sorted_senses)
                if len(sorted_senses) == 0:
                    eqSenseMap[left_vals] = None
                    break

                # iteratively search for a sense that covers k values
                potential_set = set()
                while not potential_set:
                    topk = sorted_senses[:k]
                    # print('topk:', topk)
                    Lambda = set(topk[0]).intersection(*topk)
                    if Lambda:
                        potential_set = potential_set.union(Lambda)
                    k -= 1
                    if k == 0:
                        break

                # select the sense with maximal tuple coverage
                potential_set = list(potential_set)
                selected_sense = potential_set[0]
                max_cover = self.cover(self.senses[ofd_right_attr][selected_sense], right_vals)
                for s in potential_set[1:]:
                    curr_cover = self.cover(self.senses[ofd_right_attr][s], right_vals)
                    if curr_cover > max_cover:
                        selected_sense = s
                
                # add selected sense to equivalence sense map
                eqSenseMap[left_vals] = selected_sense

            self.eqSenseList.append(eqSenseMap)

    def cover(self, sense, column):
        '''
        senses: a sense, i.e., a list of synonyms
        column: a list of values
        '''
        coverage = 0
        for item in column:
            if item in sense:
                coverage += 1

        return coverage
