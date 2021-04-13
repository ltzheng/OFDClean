from collections import Counter
import numpy as np
import itertools
from collections import ChainMap
from utils import find_sense


class DependencyGraph(object):

    def __init__(self, eqTupleNumList, eqSenseList, senseMap, overlapMap, eqTupleMap, eqRightAttrMap, threshold):
        self.eqSenseMap = dict(ChainMap(*eqSenseList))
        # self.eqSenseMap = {k: v for k, v in self.eqSenseMap.items() if v is not None}
        self.eqTupleNumMap = dict(ChainMap(*eqTupleNumList))
        # self.eqTupleNumMap = {k: v for k, v in self.eqTupleNumMap.items() if k in self.eqSenseMap}
        self.senseMap = senseMap
        self.overlapMap = overlapMap
        self.eqTupleMap = eqTupleMap
        self.eqRightAttrMap = eqRightAttrMap
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
    def BFS(self, mode):
        # start with max EMD node
        start = list(dict(sorted(self.vertex_emd.items(), key=lambda item: item[1], reverse=True)).keys())[0]
        queue = []
        queue.append(start)
        visited = set()
        visited.add(start)

        while len(queue) > 0:
            u = queue.pop(0)
            neighbors = [v for v in self.edges[u] if self.weight[(u, v)] > self.threshold]

            if mode == 'local':
                for v in neighbors:
                    if v not in visited:
                        queue.append(v)
                        visited.add(v)
                        self.local_refine(u, v)

            elif mode == 'optimal':
                for v in neighbors:
                    if v not in visited:
                        queue.append(v)
                        visited.add(v)
                        self.optimal_assign(u, v)

            else:
                raise NotImplementedError

    # locally refine sense assignments
    def local_refine(self, u, v):
        """
        u is the parent of v
        """
        self.refined_eqSenseMap = self.eqSenseMap.copy()
        val1 = self.eqTupleMap[u]
        val2 = self.eqTupleMap[v]

        # propagate v's sense to u
        new_w = self.EMD(val1, val2, self.refined_eqSenseMap[u], self.refined_eqSenseMap[u])
        if new_w < self.weight[(u, v)]:
            self.refined_eqSenseMap[v] = self.refined_eqSenseMap[u]
            self.weight[(u, v)] = new_w
            self.weight[(v, u)] = new_w

            # update edge weight of all neighbors of v
            for neighbor in self.edges[v]:
                val2 = self.eqTupleMap[neighbor]
                w = self.EMD(val1, val2, self.eqSenseMap[v], self.eqSenseMap[neighbor])
                self.weight[(v, neighbor)] = w
                self.weight[(neighbor, v)] = w

    # optimal sense assignments for accuracy measure experiments
    def optimal_assign(self, u, v):
        """
        u is the parent of v
        """
        self.optimal_eqSenseMap = {k: v for k, v in self.eqSenseMap.items()}
        val1 = self.eqTupleMap[u]
        val2 = self.eqTupleMap[v]

        # replace v's sense with u's one
        # self.optimal_eqSenseMap[v] += self.refined_eqSenseMap[u]

    # Earth mover's distance of transforming val1 to val2
    def EMD(self, val1, val2, sense1, sense2):
        # print('val1:', val1)
        # print('val2:', val2)
        # replace with the canonical value
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
    
    def replace(self, vals, sense_name):
        if isinstance(vals, list):
            for i, item in enumerate(vals):
                synonyms = find_sense(sense_name, self.senseMap)
                if item in synonyms:
                    # default the 1st value in sense
                    vals[i] = synonyms[0]
        return vals

    def display(self):
        print('\ndependency graph:', self.edges)
        print('\nedge weight:', self.weight)
        print('\nvertex weight:', self.vertex_emd)
