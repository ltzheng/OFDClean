from utils.utils import get_attribute


# graph building: append an edge if intersection exists
def build_graph(data):
    attributeA, attributeB = get_attribute(data)
    print('attributeA:', attributeA)
    print('attributeB:', attributeB)

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



# Breadth first search, return the searching order
def BFS(graph, start1, start2):
    queue = []
    queue.append(start1)
    seen = set()
    seen.add(start1)
    seen.add(start2)  # start with start1, check other neighbors (without start2) of start1
    path = []
    while len(queue) > 0:
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for node in nodes:
            if node not in seen:
                queue.append(node)
                seen.add(node)
        path.append(vertex)
    path.pop(0)  # remove start1
    return path


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

