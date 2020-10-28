import pandas as pd
from collections import Counter
import scipy.stats
import math


# get the num of functional dependencies
def get_attribute(data):
    return data['A'].unique(), data['B'].unique()


# convert element in senses to string format
def sense2str(senses):
    for i in senses:
        senses[i] = str(senses[i])
    return senses


# graph building: append an edge if intersection exists
def build_graph(data):
    attributeA, attributeB = get_attribute(data)
    # print('attributeA:', attributeA)
    # print('attributeB:', attributeB)

    # init graph
    vertexes = [i for i in range(len(attributeA) + len(attributeB))]
    graph = {}
    for i in range(len(vertexes)):
        graph[i] = []

    # build graph
    for i, attrA in zip(range(len(attributeA)), attributeA):
        intersection = []
        for j, attrB in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
            # print(data[data['A'] == attrA].index.tolist())
            # print(data[data['B'] == attrB].index.tolist())
            overlap = [ind for ind in data[data['A'] == attrA].index.tolist()
                       if ind in data[data['B'] == attrB].index.tolist()]
            if len(overlap):
                intersection.append(j)
                graph[j] += [i]
        graph[i] = intersection

    return graph


# select the optimal sense(s) for a node
def sense_select(attrC, senses):
    ontology_repair_nums = []  # numbers of ontology repair for each sense
    data_repair_nums = []  # numbers of data repair for each node

    # calculate data_repair_nums & ontology_repair_nums
    for ind in senses:
        synonyms = senses[ind]
        data_repair_num = 0
        ontology_repair_num = 0
        for attr in attrC:
            attr = str(attr)
            if attr not in senses[ind]:
                data_repair_num += 1
            if attr not in synonyms:
                ontology_repair_num += 1
                synonyms += attr
        ontology_repair_nums.append(ontology_repair_num)
        data_repair_nums.append(data_repair_num)
    # print('ontology_repair_nums:', ontology_repair_nums)
    # print('data_repair_nums:', data_repair_nums)

    min_ont_sense = [ind for ind, val in enumerate(ontology_repair_nums) if val == min(ontology_repair_nums)]
    min_data_sense = [ind for ind, val in enumerate(data_repair_nums) if val == min(data_repair_nums)]
    optimal_sense = list(set(min_ont_sense).intersection(set(min_data_sense))) # there exists 1 optimal sense
    if not optimal_sense:  # if more than 1 sense
        optimal_sense = list(set(min_ont_sense).union(set(min_data_sense)))

    # print('min_ont_sense:', min_ont_sense)
    # print('min_data_sense:', min_data_sense)
    # print('optimal_sense:', optimal_sense)

    return optimal_sense


# return a dict describing optimal sense(s) for each node
def optimal_senses(data, senses):
    senses_dict = {}
    attributeA, attributeB = get_attribute(data)
    for i, attr in zip(range(len(attributeA)), attributeA):
        senses_dict[i] = sense_select(data[data['A'] == attr]['C'].tolist(), senses)
    for i, attr in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
        senses_dict[i] = sense_select(data[data['B'] == attr]['C'].tolist(), senses)

    return senses_dict


# return table of probability for each node
def prob_table(data, senses):
    attributeA, attributeB = get_attribute(data)
    nodes = [i for i in range(len(attributeA) + len(attributeB))]

    synonyms = []
    for ind in senses:
        synonyms += senses[ind]
    synonyms = list(set(synonyms))
    # print('synonyms:', synonyms)
    prob = pd.DataFrame(index=nodes, columns=synonyms)
    prob.loc[:, :] = 0

    for i, attr in zip(range(len(attributeA)), attributeA):
        attrC = data[data['A'] == attr]['C'].tolist()
        # print('attrC:', attrC)
        counter = Counter(attrC)
        # print('counter:', counter)
        for f in counter:
            prob.loc[i, str(f)] = counter[f] / len(attrC)
    for i, attr in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
        attrC = data[data['B'] == attr]['C'].tolist()
        # print('attrC:', attrC)
        counter = Counter(attrC)
        # print('counter:', counter)
        for f in counter:
            prob.loc[i, str(f)] = counter[f] / len(attrC)

    return prob


# calculate KL-divergence of 2 probability distribution for nodes in graph
# return sorted (by KL-divergence) array with 2 nodes attached
def KL_table(graph, prob):
    # # dict-format table
    # # e.g., {0: {2: 0.11167592062840895}, 1: {2: inf, 3: inf}, 2: {0: 0.10926010165375145, 1: inf}, 3: {1: 0.4620981203732968}}
    # table = {}
    # for i in graph:
    #     table[i] = {}
    # for node_x in graph:
    #     for node_y in graph[node_x]:
    #         # print(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())
    #         table[node_x][node_y] = scipy.stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())

    # # DataFrame-format table
    # table = pd.DataFrame(index=graph.keys(), columns=graph.keys())
    # for node_x in graph:
    #     for node_y in graph[node_x]:
    #         table.iloc[node_x, node_y] = scipy.stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())

    # list-format table
    table = []
    for node_x in graph:
        for node_y in graph[node_x]:
            KL = scipy.stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())
            table.append([KL, node_x, node_y])

    return sorted(table, key=(lambda x: x[0]), reverse=False)  # sort by KL-divergence decreasing order


# def baseline(KLtable, optimal):
#     sense_assign = []
#     temp_assign = {}
#     for KL in KLtable:
#         if optimal[KL[2]] not in temp_assign:
#             temp_assign[KL[1]] = [optimal[KL[2]]]
#             temp_assign[KL[2]] = [optimal[KL[2]]]
#         else:
#             temp = temp_assign
#             temp[KL[1]] = [optimal[KL[2]]]
#             temp[KL[2]] = [optimal[KL[2]]]


# # Breadth first search, return the searching order
# def BFS(graph, start1, start2):
#     queue = []
#     queue.append(start1)
#     seen = set()
#     seen.add(start1)
#     seen.add(start2)  # start with start1, check other neighbors (without start2) of start1
#     path = []
#     while len(queue) > 0:
#         vertex = queue.pop(0)
#         nodes = graph[vertex]
#         for node in nodes:
#             if node not in seen:
#                 queue.append(node)
#                 seen.add(node)
#         path.append(vertex)
#     path.pop(0)  # remove start1
#     return path


# recursive dfs
def dfs(graph, start, queue):
    if queue is None:
        queue = []
    queue.append(start)
    for neighbor in graph[start]:
        if neighbor not in queue:
            dfs(graph, neighbor, queue)
    # print('queue:', queue)
    return queue


# non-recursive dfs
# def DFS(graph, start):
#     stack = [start]
#     visited = set()
#     visited.add(start)
#     while stack:
#         node = stack.pop()
#         for neighbor in graph[node]:
#             if neighbor not in visited:
#                 stack.append(neighbor)
#                 visited.add(neighbor)


# find all connected component, return a list containing connected nodes
def find_cc(graph):
    all_cc = []
    visited = []
    for v in graph:
        if v not in visited:
            cc = dfs(graph, v, None)
            visited += cc
            all_cc.append(cc)
    # print(all_cc)
    return all_cc


# build a graph w.r.t. KL-divergence
def sense_graph(org_graph, KLtable, threshold=float("inf")):
    new_graph = {}
    for v in org_graph:
        new_graph[v] = []
    for KL in KLtable:
        if not math.isinf(KL[0]):
            if math.isinf(threshold) or KL[0] < threshold:
                if KL[2] not in new_graph[KL[1]]:
                    new_graph[KL[1]] += [KL[2]]
                if KL[1] not in new_graph[KL[2]]:
                    new_graph[KL[2]] += [KL[1]]
    # print('new_graph:', new_graph)
    return new_graph


def sense_assign(graph, KLtable, optimal, threshold=float("inf")):
    possible_assign = {}
    all_cc = find_cc(sense_graph(graph, KLtable, threshold))
    # print('all_cc:', all_cc)
    for cc in all_cc:
        possible_assign[tuple(cc)] = []
        for node in cc:
            possible_assign[tuple(cc)] += optimal[node]
    for i in possible_assign:
        possible_assign[i] = list(set(possible_assign[i]))
    print('possible_assign:', possible_assign)



# def minKL(graph, KLtable, optimal, threshold):
#     sense_assign = []
#     temp_assign = {}
#     path = BFS(graph, KLtable[0][1], KLtable[0][2])
#     for KL in KLtable:
#         node_x = KL[1]
#         node_y = KL[2]
#         for sense_x in optimal[node_x]:  # traverse all optimal senses
#             temp_assign[node_x] = sense_x  # assign nodeX with its optimal sense
#             if KL[0] < threshold:
#                 temp_assign[node_y] = optimal[node_x]
#             if KL[0] > threshold:
#                 for sense_y in optimal[node_y]:  # traverse all optimal senses
#                     temp_assign[node_y] = sense_y



if __name__ == '__main__':
    data_path = 'data.csv'
    senses_path = 'senses.csv'
    test_threshold = 0.2

    test_data = pd.read_csv(data_path)
    senses_table = pd.read_csv(senses_path, header=None, index_col=0)
    test_senses = senses_table.to_dict()[1]
    test_senses = sense2str(test_senses)
    print('senses:', test_senses)

    # print(data['C'].tolist())
    # print(data[data['A'] == attributeA[0]]['C'])

    test_graph = build_graph(test_data)
    print('graph:', test_graph)

    opt = optimal_senses(test_data, test_senses)
    print('optimal_senses:', opt)

    '''example output
    senses: {1: '123', 2: '24', 3: '145', 4: '235', 5: '125'}
    graph: {0: [2], 1: [2, 3], 2: [0, 1], 3: [1]}
    optimal_senses: {0: [0], 1: [3], 2: [0, 1], 3: [3]}
    '''

    print('prob_table:\n', prob_table(test_data, test_senses))

    KLtab = KL_table(test_graph, prob_table(test_data, test_senses))
    print('KL_table:', KLtab)

    # minKL(KLtab, optimal_senses(test_data, test_senses), test_threshold)
    #
    # BFS(test_graph, 0)

    # print('baseline:', baseline(KLtab, opt))

    sense_assign(test_graph, KLtab, opt)

    sense_assign(test_graph, KLtab, opt, test_threshold)
