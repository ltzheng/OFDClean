from collections import Counter
import numpy as np


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

    def __init__(self, eqTupleMap, eqSenseMap, attrs1, attrs2, 
                 sense_dict, right_col_name, threshold,
                 col_name1='A', col_name2='B'):
        """
        attr: a list of attribute values of x
        sense: sense assignment map
        sense_dict: map sense id->value synonyms list
        """
        self.attrs1 = attrs1
        self.attrs2 = attrs2
        self.attrs = np.concatenate((attrs1, attrs2))
        print('attrs:', self.attrs)

        self.col_name1 = col_name1
        self.col_name2 = col_name2
        self.data = data
        self.threshold = threshold
        self.right_col_name = right_col_name
        self.sense_dict = sense_dict

        self.initial_senses1 = initial_senses1
        self.sense_assignment = {}
        for d in (initial_senses1, initial_senses2):
            self.sense_assignment.update(d)

        self.vertexes = [i for i in range(len(self.sense_assignment))]
        self.adj = {}
        self.weight = {}
        self.vertex_emd = {}
        for i in range(len(self.vertexes)):
            self.adj[i] = []
            self.vertex_emd[i] = 0

        # edge exists when overlap
        for i, attr1 in enumerate(self.attrs1):
            for j, attr2 in zip(range(len(self.attrs1), len(self.attrs)), self.attrs2):
                x1 = self.data[self.data[self.col_name1] == attr1]
                x2 = self.data[self.data[self.col_name2] == attr2]
                if len(self.overlap_tuples(x1, x2)):
                    self.adj[i] += [j]
                    self.adj[j] += [i]

                    # w(u1, u2) is the EMD between u1 and u2
                    # w = EMD(self.distribution(x1[self.right_col_name].tolist(), self.sense_assignment[attr1]), 
                    #         self.distribution(x2[self.right_col_name].tolist(), self.sense_assignment[attr2]))
                    val1 = x1[self.right_col_name].tolist()
                    val2 = x2[self.right_col_name].tolist()
                    w = self.EMD(val1, val2, self.sense_assignment[attr1], self.sense_assignment[attr2])
                    self.weight[(i, j)] = w
                    self.weight[(j, i)] = w
                    self.vertex_emd[i] += w
                    self.vertex_emd[j] += w

    def BFS(self):
        start = list(dict(sorted(self.vertex_emd.items(), key=lambda item: item[1], reverse=True)).keys())[0]
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
                    self.local_refine(vertex, node)
                if node not in seen:
                    queue.append(node)
                    seen.add(node)
            path.append(vertex)
        path.pop(0)  # remove start
        
        return path

    # compute overlapping tuples
    def overlap_tuples(self, x1, x2):
        """
        attr: names of attributes
        """
        overlap_index = [ind for ind in x1.index.tolist() if ind in x2.index.tolist()]
        overlap = self.data.loc[overlap_index, :]

        # print('x1:\n', x1)
        # print('x2:\n', x2)
        # print('overlap:\n', overlap)
        return overlap

    # locally refine sense assignments
    def local_refine(self, u, v):
        """
        data: dataframe
        u, v: vertexes in G
        col_name1, col_name2: column name of x1, x2
        sense1, sense2: sense of x1, x2
        sense_dict: map sense id->value synonyms
        """
        sense1 = self.node2sense(u)
        sense2 = self.node2sense(v)
        attr1 = self.node2attr(u)
        attr2 = self.node2attr(v)
        print('attr1:', attr1)
        print('attr2:', attr2)
        x1 = self.node2x(u)
        x2 = self.node2x(v)
        print('x1:\n', x1)
        print('x2:\n', x2)
        val1 = x1[self.right_col_name].values.tolist()
        val2 = x2[self.right_col_name].values.tolist()

        overlap = self.overlap_tuples(x1, x2)[self.right_col_name].values.tolist()
        reassign_cost1 = sense_reassign_cost(val1, sense1, sense2, self.sense_dict)
        reassign_cost2 = sense_reassign_cost(val2, sense2, sense1, self.sense_dict)

        if min(reassign_cost1, reassign_cost2) < repair_cost(overlap, sense1, sense2, self.sense_dict):
            if reassign_cost1 > reassign_cost2:
                # new_w = EMD(self.distribution(attr2, self.sense_dict[self.sense_assignment[attr2]]), self.distribution(attr2, sense1))
                new_w = self.EMD(val2, val2, self.sense_assignment[attr2], sense1)
                print('sense1:', self.sense_assignment[attr2])
                print('sense2:', sense1)
                if new_w < self.weight[(u, v)]:
                    self.sense_assignment[attr2] = sense1
                    self.weight[(u, v)] = new_w
                    self.weight[(v, u)] = new_w
            else:
                # new_w = EMD(self.distribution(attr1, self.sense_dict[self.sense_assignment[attr1]]), self.distribution(attr1, sense2))
                new_w = self.EMD(val1, val1, self.sense_assignment[attr1], sense2)
                print('sense1:', self.sense_assignment[attr1])
                print('sense2:', sense2)
                if new_w < self.weight[(u, v)]:
                    self.sense_assignment[attr1] = sense2
                    self.weight[(u, v)] = new_w
                    self.weight[(v, u)] = new_w

    # Earth mover's distance of transforming val1 to val2
    def EMD(self, val1, val2, sense1, sense2):
        print('val1:', val1)
        print('val2:', val2)
        val1, val2 = self.replace(val1, sense1), self.replace(val2, sense2)
        d = dict.fromkeys(list(set(np.concatenate((val1, val2)))))
        dist1 = {x: 0 for x in d}
        dist2 = dist1.copy()
        dist1.update(dict(Counter(val1)))
        dist2.update(dict(Counter(val2)))
        print('dist1:', dist1)
        print('dist2:', dist2)

        emds = []
        emds.append(0)
        dist1, dist2 = list(dist1.values()), list(dist2.values())
        for i, p_i, q_i in zip(range(len(dist1)), dist1, dist2):
            emds.append(p_i + emds[i] - q_i)
        emd = sum(abs(number) for number in emds)
        print('EMDs:', emds)
        print('emd:', emd)

        return emd
    
    def replace(self, vals, sense):
        if isinstance(vals, list):
            for i, item in enumerate(vals):
                # replace with canonical values (default: 1st value in sense)
                if item in sense:
                    vals[i] = sense[0]
        return vals

    def node2sense(self, u):
        return list(self.sense_assignment.values())[u]

    def node2attr(self, u):
        return self.attrs[u]

    def node2x(self, u):
        attr = self.attrs[u]
        if u < len(self.initial_senses1):
            return self.data[self.data[self.col_name1] == attr]
        else:
            return self.data[self.data[self.col_name2] == attr]

    def display(self):
        print('\ndependency graph:', self.adj)
        print('\nedge weight:', self.weight)
        print('\nvertex weight:', self.vertex_emd)
        print('\nsense assignment:\n', self.sense_assignment)


# # compute distribution
# def distribution(vals, sense):
#     print('\nsynonyms:', sense)
#     print('before replace:', vals)

#     if isinstance(vals, list):
#         for i, item in enumerate(vals):
#             # replace with canonical values (default: 1st value in sense)
#             if item in sense:
#                 vals[i] = sense[0]

#     print('after replace:', vals)
    
#     d = dict(Counter(vals))
#     print('distribution:', d)
#     return d