from utils.utils import get_attribute
from scipy.stats import wasserstein_distance
from collections import Counter


# compute distribution
def distribution(attr, sense, sense_dict):
    '''
    attr: a list of attribute of x
    senses: a sense, i.e., a list of synonyms
    '''
    for i, item in enumerate(attr):
        # replace with canonical values (default: 1st value in sense)
        print('attr:', attr)
        if item in sense_dict[sense]:
            attr[i] = sense_dict[sense][0]
        print('attr:', attr)
    
    d = dict(Counter(attr))
    return d


# compute earth mover's distance
def EMD(P, Q):
    '''
    P, Q: dict from distribution function
    '''
    P, Q = list(P.values()), list(Q.values())
    wasserstein_distance(P, Q)
    return 


def compute_cost():
    raise NotImplementedError


class DependencyGraph(object):

    def __init__(self, data, initial_senses1, initial_senses2, attrs1, attrs2, 
                 sense_dict, right_col_name,
                 col_name1='A', col_name2='B', threshold=0.2):
        self.attrs1 = attrs1
        self.attrs2 = attrs2
        self.col_name1 = col_name1
        self.col_name2 = col_name2
        self.data = data
        self.threshold = threshold
        self.right_col_name = right_col_name

        self.vertexes = [i for i in range(len(initial_senses1) + len(initial_senses2))]
        self.adj = {}
        self.weight = {}
        for i in range(len(self.vertexes)):
            self.adj[i] = []

        # edge exists when overlap
        for i, x1 in zip(range(len(attrs1)), attrs1):
            for j, x2 in zip(range(len(attrs2), len(attrs1) + len(attrs2)), attrs2):
                if len(self.overlap_tuples(x1, x2)):
                    self.adj[i] += [j]
                    self.adj[j] += [i]

                    # w(u1, u2) is the EMD between u1 and u2
                    w = EMD(distribution(self.data[self.data[self.col_name1] == x1][self.right_col_name], initial_senses1[x1], sense_dict),
                            distribution(self.data[self.data[self.col_name2] == x2][self.right_col_name], initial_senses2[x2], sense_dict))
                    self.weight[(i, j)] = w
                    self.weight[(j, i)] = w


    # compute overlapping tuples
    def overlap_tuples(self, x1, x2):
        overlap = [ind for ind in self.data[self.data[self.col_name1] == x1].index.tolist()
                        if ind in self.data[self.data[self.col_name2] == x2].index.tolist()]
        return overlap

    # Algorithm 2: Local Refinement
    def BFS(self, start):
        queue = []
        queue.append(start)
        seen = set()
        seen.add(start)
        path = []

        while len(queue) > 0:
            vertex = queue.pop(0)
            nodes = self.adj[vertex]
            for node in nodes:
                if self.weight[(vertex, node)] > self.threshold:
                    # TODO
                    compute_cost()
                    # TODO: Algorithm 2
                if node not in seen:
                    queue.append(node)
                    seen.add(node)
            path.append(vertex)
        path.pop(0)  # remove start
        
        return path
