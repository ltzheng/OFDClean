
def local_refinement(data, Lambda):
    u = BFS(build_graph(data))
    for v in u


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
    optimal_sense = list(set(min_ont_sense).intersection(set(min_data_sense)))  # there exists 1 optimal sense
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


# return table of probability for each node
def prob_table(data, senses):
    attributeA, attributeB = get_attribute(data)
    nodes = [i for i in range(len(attributeA) + len(attributeB))]

    synonyms = []
    for ind in senses:
        synonyms += senses[ind]
    synonyms = list(set(synonyms))
    # print('synonyms:', synonyms)
    prob = dict(index=nodes, columns=synonyms)
    prob.loc[:, :] = 0

    for i, attr in zip(range(len(attributeA)), attributeA):
        attrC = data[data['A'] == attr]['C'].tolist()
        prob.loc[i, :] = frequency(attrC)
    for i, attr in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
        attrC = data[data['B'] == attr]['C'].tolist()


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
    #         table[node_x][node_y] = stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())

    # # DataFrame-format table
    # table = pd.DataFrame(index=graph.keys(), columns=graph.keys())
    # for node_x in graph:
    #     for node_y in graph[node_x]:
    #         table.iloc[node_x, node_y] = stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())

    # list-format table
    table = []
    for node_x in graph:
        for node_y in graph[node_x]:
            KL = stats.entropy(prob.loc[node_x].tolist(), prob.loc[node_y].tolist())
            table.append([KL, node_x, node_y])

    return sorted(table, key=(lambda x: x[0]), reverse=False)  # sort by KL-divergence decreasing order


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
