import pandas as pd
import argparse
from utils.data_reader import DataLoader
from algorithms.ontology_repair import OntologyRepair
from algorithms.data_repair import DataRepair
from algorithms.dependency_graph import DependencyGraph


class OFDClean(object):

    def __init__(self, data, ontology, senses):
        self.data = data
        self.ontology = ontology
        self.senses = senses

        self.getEquivalenceClass()
        
        self.ontCandidate = {}

        self.OntRepair = OntologyRepair()
        self.DataRepair = DataRepair()

    def getEquivalenceClass(self):
        self.eqTupleMap = {}

    def run(self):
        self.init_assign()

        DependencyGraph = DependencyGraph(self.eqSenseMap)
        self.refined_eqSenseMap = DependencyGraph.local_refine()

        self.getPretoOptimalSolution()

    # Algorithm 1: assign a local optimal sense to each equivalence class
    def init_assign(x, ssets, sense_dict):
        '''
        x: an equivalent class, i.e., a dataframe with 2 columns (left values are the same)
        ssets: map value->senses
        sense_dict: map sense->synonym values
        '''
        self.eqSenseMap = {}

        right_attr = x.iloc[:, -1].tolist()
        print('right attribute:', right_attr)
        freq = dict(Counter(right_attr))

        # k = stats.median_absolute_deviation(list(freq.values()))
        # print('k:', k)
        # MAD = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

        # sort values by deviation from median frequency
        print('freq:', freq)
        median_freq = median(freq.values())
        deviation = {k: abs(v - median_freq) for k, v in freq.items()}
        deviation = dict(sorted(deviation.items(), key=lambda item: item[1], reverse=False))
        print('deviation:', deviation)

        k = len(deviation)
        print('k=', k)

        sorted_senses = []
        sorted_synonyms = list(deviation.keys())
        for syn in sorted_synonyms:
            if syn in ssets.keys():
                print('syn:', syn)
                print('ssets[syn]', ssets[syn])
                if ssets[syn] not in sorted_senses:
                    sorted_senses.append(ssets[syn])
        print('sorted_synonyms', sorted_synonyms)
        print('sorted_senses', sorted_senses)

        # iteratively search for a sense that covers k values
        potential_set = set()
        while not potential_set:
            topk = sorted_senses[:k]
            print('topk:\n', topk)
            Lambda = set(topk[0]).intersection(*topk)
            if Lambda:
                potential_set = potential_set.union(Lambda)
            k -= 1
            if k == 0:
                break

        # select the sense with maximal tuple coverage
        potential_set = list(potential_set)
        selected_sense = potential_set[0]
        max_cover = cover(sense_dict[selected_sense], right_attr)
        for s in potential_set[1:]:
            curr_cover = cover(sense_dict[s], right_attr)
            if curr_cover > max_cover:
                selected_sense = s

    def getPretoOptimalSolution():
        return

if __name__ == '__main__':
    Loader = DataLoader(config)
    data = Loader.read_data()
    ontology = Loader.read_ontology()
    senses = Loader.read_senses()

    Cleaner = OFDClean(data, ontology, senses)
    Cleaner.run()