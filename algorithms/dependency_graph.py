from collections import Counter
import numpy as np
import itertools
from collections import ChainMap


# get the num of functional dependencies
def get_attribute(data, col_name):
    return data[col_name].unique()


# compute outliers w.r.t a given sense and values
def outliers(vals, sense, sense_dict):
    """
    vals: a list of attribute values of Omega (overlap set)
    sense: a sense, i.e., a list of synonyms
    sense_dict: map sense id->value synonyms
    """
    outlier_set = set()
    total_outlier_num = 0

    print('\nsynonyms:', sense)
    print('vals:', vals)

    if vals:
        for item in vals:
            if item not in sense:
                outlier_set.add(item)
                total_outlier_num += 1
        outlier_set = list(outlier_set)
        print('outliers:', outlier_set)
    else:
        outlier_set = []

    return outlier_set, total_outlier_num


def repair_cost(vals, sense1, sense2, sense_dict):
    """
    vals: a list of attribute values of Omega (overlap set)
    sense1, sense2: lists of synonyms
    sense_dict: map sense id->value synonyms
    """
    rho1, R1 = outliers(vals, sense1, sense_dict)
    rho2, R2 = outliers(vals, sense2, sense_dict)

    # ontology repair cost
    ontology_repair_cost = len(rho1) + len(rho2)  # number of unique outlier values

    # data_repair_cost
    data_repair_cost = R1 + R2

    return min(ontology_repair_cost, data_repair_cost)


def sense_reassign_cost(vals, sense1, sense2, sense_dict):
    """
    vals: a list of attribute values of x
    sense1, sense2: lists of synonyms
    sense_dict: map sense id->value synonyms
    """
    _, R1 = outliers(vals, sense1, sense_dict)
    _, R2 = outliers(vals, sense2, sense_dict)
    cost = R2 - R1
    return cost


class DependencyGraph(object):

    def __init__(self, eqTupleNumList, eqSenseList, senses, overlapMap, eqTupleMap, threshold):
        self.eqSenseMap = dict(ChainMap(*eqSenseList))
        # self.eqSenseMap = {k: v for k, v in self.eqSenseMap.items() if v is not None}
        self.eqTupleNumMap = dict(ChainMap(*eqTupleNumList))
        # self.eqTupleNumMap = {k: v for k, v in self.eqTupleNumMap.items() if k in self.eqSenseMap}
        self.senses = senses
        self.overlapMap = overlapMap
        self.eqTupleMap = eqTupleMap
        self.threshold = threshold

        # build the dependency graph
        self.vertexes = []
        for eqTuple in self.eqTupleNumMap.keys():
            self.vertexes.append(eqTuple)

        # adjacent lists
        self.edges = {k: [] for k in self.vertexes}
        self.vertex_emd = {k: 0 for k in self.vertexes}
        self.weight = {}  # w(u1, u2) is the EMD between u1 and u2

        for num, senses in self.overlapMap.items():
            # edge exists when classes overlap
            pairs = list(itertools.combinations(senses, 2))
            for pair in pairs:
                # print('pair:', pair)
                u = pair[0]
                v = pair[1]
                if not self.eqSenseMap[u] or not self.eqSenseMap[v]:
                    continue
                if v in self.edges[u]:
                    continue
                self.edges[u] += [v]
                self.edges[v] += [u]

                # EMD as weight
                val1 = self.eqTupleMap[u]
                val2 = self.eqTupleMap[v]
                w = self.EMD(val1, val2, self.eqSenseMap[u], self.eqSenseMap[v])
                self.weight[(u, v)] = w
                self.weight[(v, u)] = w
                self.vertex_emd[u] += w
                self.vertex_emd[v] += w

    # breadth-first traverse the dependency graph
    def BFS(self):
        start = list(dict(sorted(self.vertex_emd.items(), key=lambda item: item[1], reverse=True)).keys())[0]
        queue = []
        queue.append(start)  # start with max EMD node
        visited = set()
        visited.add(start)
        self.refined_eqSenseMap = self.eqSenseMap.copy()

        while len(queue) > 0:
            u = queue.pop(0)
            neighbors = [v for v in self.edges[u] if self.weight[(u, v)] > self.threshold]
            for v in neighbors:
                self.local_refine(u, v)
                if v not in visited:
                    queue.append(v)
                    visited.add(v)

    # locally refine sense assignments
    def local_refine(self, u, v):
        val1 = self.eqTupleMap[u]
        val2 = self.eqTupleMap[v]
        # replace u's sense with v's one
        new_w = self.EMD(val1, val2, self.refined_eqSenseMap[v], self.refined_eqSenseMap[v])
        if new_w < self.weight[(u, v)]:
            self.refined_eqSenseMap[u] = self.refined_eqSenseMap[v]

    # optimal sense assignments for accuracy measure experiments
    def optimal_assign(self):
        start = list(dict(sorted(self.vertex_emd.items(), key=lambda item: item[1], reverse=True)).keys())[0]
        queue = []
        queue.append(start)  # start with max EMD node
        visited = set()
        visited.add(start)
        self.optimal_eqSenseMap = self.eqSenseMap.copy()

        while len(queue) > 0:
            u = queue.pop(0)
            neighbors = [v for v in self.edges[u] if self.weight[(u, v)] > self.threshold]
            for v in neighbors:
                val1 = self.eqTupleMap[u]
                val2 = self.eqTupleMap[v]
                # replace u's sense with v's one
                new_w = self.EMD(val1, val2, self.optimal_eqSenseMap[v], self.optimal_eqSenseMap[v])
                
                self.optimal_eqSenseMap[u] = self.optimal_eqSenseMap[v]
                
                if v not in visited:
                    queue.append(v)
                    visited.add(v)


        # overlap = self.overlap_tuples(x1, x2)[self.right_col_name].values.tolist()
        # reassign_cost1 = sense_reassign_cost(val1, sense1, sense2, self.sense_dict)
        # reassign_cost2 = sense_reassign_cost(val2, sense2, sense1, self.sense_dict)
        # if min(reassign_cost1, reassign_cost2) < repair_cost(overlap, sense1, sense2, self.sense_dict):
        #     if reassign_cost1 > reassign_cost2:
        #         # new_w = EMD(self.distribution(attr2, self.sense_dict[self.sense_assignment[attr2]]), self.distribution(attr2, sense1))
        #         new_w = self.EMD(val2, val2, self.sense_assignment[attr2], sense1)
        #         print('sense1:', self.sense_assignment[attr2])
        #         print('sense2:', sense1)
        #         if new_w < self.weight[(u, v)]:
        #             self.sense_assignment[attr2] = sense1
        #             self.weight[(u, v)] = new_w
        #             self.weight[(v, u)] = new_w
        #     else:
        #         # new_w = EMD(self.distribution(attr1, self.sense_dict[self.sense_assignment[attr1]]), self.distribution(attr1, sense2))
        #         new_w = self.EMD(val1, val1, self.sense_assignment[attr1], sense2)
        #         print('sense1:', self.sense_assignment[attr1])
        #         print('sense2:', sense2)
        #         if new_w < self.weight[(u, v)]:
        #             self.sense_assignment[attr1] = sense2
        #             self.weight[(u, v)] = new_w
        #             self.weight[(v, u)] = new_w

    # Earth mover's distance of transforming val1 to val2
    def EMD(self, val1, val2, sense1, sense2):
        # print('val1:', val1)
        # print('val2:', val2)
        # replace with canonical values
        val1, val2 = self.replace(val1, sense1), self.replace(val2, sense2)

        # compute distributions
        dist1 = {k: 0 for k in list(set(np.concatenate((val1, val2))))}
        dist2 = dist1.copy()
        dist1.update(dict(Counter(val1)))
        dist2.update(dict(Counter(val2)))
        # print('dist1:', dist1)
        # print('dist2:', dist2)

        # compute emd by dynamic programming
        emds = []
        emds.append(0)
        dist1, dist2 = list(dist1.values()), list(dist2.values())
        for i, p_i, q_i in zip(range(len(dist1)), dist1, dist2):
            emds.append(p_i + emds[i] - q_i)
        emd = sum(abs(number) for number in emds)
        # print('EMDs:', emds)
        # print('emd:', emd)

        return emd
    
    def replace(self, vals, sense):
        if isinstance(vals, list):
            for i, item in enumerate(vals):
                # default the 1st value in sense
                if item in sense:
                    vals[i] = sense[0]
        return vals

    def display(self):
        print('\ndependency graph:', self.edges)
        print('\nedge weight:', self.weight)
        print('\nvertex weight:', self.vertex_emd)
        # print('\nsense assignment:\n', self.sense_assignment)
