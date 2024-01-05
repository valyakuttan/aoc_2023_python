from puzzle import *

def test_neighbors():
    with open('sample.input', 'r') as file:
        data = file.read()

    start, nodes = parse_input(data, NodeType.FSH)
    pos_to_nodes = {node.node[0]: node for node in nodes}

    h1 = pos_to_nodes[(1, 2)]
    v1 = pos_to_nodes[((2, 1))]   
    assert neighbors(start, pos_to_nodes) == [h1, v1]

    sv1 = pos_to_nodes[(1, 3)]
    assert neighbors(h1, pos_to_nodes) == [start, sv1]

    l1 = pos_to_nodes[(3, 1)]
    assert neighbors(v1, pos_to_nodes) == [start, l1]

    v2 = pos_to_nodes[(2, 3)]
    assert neighbors(sv1, pos_to_nodes) == [h1, v2]

    h2 = pos_to_nodes[(3, 2)]
    assert neighbors(l1, pos_to_nodes) == [v1, h2]

    j1 = pos_to_nodes[(3, 3)]
    assert neighbors(v2, pos_to_nodes) == [sv1, j1]

    assert neighbors(j1, pos_to_nodes) == [v2, h2]


def test_sample1():
    with open('sample1.input', 'r') as file:
        data = file.read()

    start, nodes = parse_input(data, NodeType.FSH)
    pos_to_nodes = {node.node[0]: node for node in nodes}

    kvs = ((n, neighbors(n, pos_to_nodes)) for n in nodes)
    graph = {k: v for k, v in kvs if len(v) == 2}

    vs = bfs(graph, start)
    max_distance = max(map(lambda x: x[1], vs))
    #print(max_distance)
    assert max_distance == 4

def test_sample2():
    with open('sample2.input', 'r') as file:
        data = file.read()

    start, nodes = parse_input(data, NodeType.FSH)
    pos_to_nodes = {node.node[0]: node for node in nodes}

    kvs = ((n, neighbors(n, pos_to_nodes)) for n in nodes)
    graph = {k: v for k, v in kvs if len(v) == 2}

    vs = bfs(graph, start)
    max_distance = max(map(lambda x: x[1], vs))
    #print(max_distance)
    assert max_distance == 8

def test():
    test_neighbors()
    test_sample1()
    test_sample2()

if __name__ == "__main__":
    test()
