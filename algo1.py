import pandas as pd


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
    optimal_sense = list(set(min_ont_sense).intersection(set(min_data_sense)))
    if not optimal_sense:  # more than 1 sense selected
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
        senses_dict[i] = sense_select(test_data[test_data['A'] == attr]['C'].tolist(), senses)
    for i, attr in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
        senses_dict[i] = sense_select(test_data[test_data['B'] == attr]['C'].tolist(), senses)

    return senses_dict


def BFS(graph, s):
    queue = []
    queue.append(s)
    seen = set()
    seen.add(s)
    while len(queue) > 0:
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for node in nodes:
            if node not in seen:
                queue.append(node)
                seen.add(node)
        print(vertex)


data_path = 'data.csv'
senses_path = 'senses.csv'

test_data = pd.read_csv(data_path)
senses_table = pd.read_csv(senses_path, header=None, index_col=0)
test_senses = senses_table.to_dict()[1]
test_senses = sense2str(test_senses)
print('senses:', test_senses)

# print(data['C'].tolist())
# print(data[data['A'] == attributeA[0]]['C'])

test_graph = build_graph(test_data)
print('graph:', test_graph)

print('optimal_senses:', optimal_senses(test_data, test_senses))

# BFS(test_graph, 'a')
