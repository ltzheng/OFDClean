import pandas as pd

data_path = 'data.csv'
senses_path = 'senses.csv'

data = pd.read_csv(data_path)
senses_table = pd.read_csv(senses_path, header=None, index_col=0)
senses = senses_table.to_dict()[1]
for i in senses:
    senses[i] = str(senses[i])
print('senses:', senses)


# print(data['C'].tolist())
# print(data[data['A'] == attributeA[0]]['C'])

# graph building: append an edge if intersection exists
def build_graph(data):
    attributeA = data['A'].unique()
    attributeB = data['B'].unique()
    # print('attributeA:', attributeA)
    # print('attributeB:', attributeB)

    vertexes = [i for i in range(len(attributeA) + len(attributeB))]
    graph = {}
    for i in range(len(vertexes)):
        graph[i] = []

    for i, attrA in zip(range(len(attributeA)), attributeA):
        intersection = []
        for j, attrB in zip(range(len(attributeA), len(attributeA) + len(attributeB)), attributeB):
            # print(data[data['A'] == attrA].index.tolist())
            # print(data[data['B'] == attrB].index.tolist())
            overlap = [i for i in data[data['A'] == attrA].index.tolist() if i in data[data['B'] == attrB].index.tolist()]
            if len(overlap):
                intersection.append(j)
                graph[j] += [i]
        graph[i] = intersection

    return graph

graph = build_graph(data)
print('graph:', graph)


def sense_select(attrC, senses):
    ontology_repair_nums = []
    data_repair_nums = []
    # print(senses)
    for i in senses:
        synonyms = senses[i]
        data_repair_num = 0
        ontology_repair_num = 0
        for attr in attrC:
            attr = str(attr)
            if attr not in senses[i]:
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
    optimal_sense = list(set(min_ont_sense).union(set(min_data_sense)))

    return optimal_sense


# for i, attr in zip(range(len(attributeA)), attributeA):
#     sense_select(data[data['A'] == attr]['C'].tolist(), senses)
#
# for i, attr in zip(range(len(attributeB)), attributeB):
#     sense_select(data[data['B'] == attr]['C'].tolist(), senses)


# print(graph)

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


# BFS(graph, 'a')
