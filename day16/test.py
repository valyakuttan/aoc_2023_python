from squaregrid import Node, SquareGrid, Direction, reconstruct_path, next_pos
from puzzle import breadth_first_search
from typing import List

def test_bfs():
    with open('sample.input', 'r') as file:
        data = file.read()

    xss = list(data.split('\n'))

    n = len(xss)
    grid = SquareGrid(n, n)
    node_map = {(i, j): ((i, j), c) for i, xs in enumerate(xss)
                for j, c in enumerate(xs)}
    grid.node_map = node_map
    #start = node_map[(7,6)]
    #c, m = breadth_first_search(grid, start, Direction.S)

    start = node_map[(0,0)]
    m = breadth_first_search(grid, start, Direction.E)
    s = set(k[0] for k in m)
    assert len(s) == 46

def path_to_str(path: List[Node]) -> str:
    return ' => '.join(p[1] for p in path)
def test_neighbors():
    with open('sample.input', 'r') as file:
        data = file.read()

    xss = list(data.split('\n'))

    n = len(xss)
    grid = SquareGrid(n, n)
    node_map = {(i, j): ((i, j), c) for i, xs in enumerate(xss)
                for j, c in enumerate(xs)}
    grid.node_map = node_map

    start = node_map[(0,0)]
    assert grid.neighbors(start, Direction.E) == [(((0, 1), '|'), Direction.E)]
    node01, d = grid.neighbors(start, Direction.E)[0]

    assert grid.neighbors(node01, Direction.S) == [(((1, 1), '.'), Direction.S)]
    assert grid.neighbors(node01, Direction.N) == []

    fs74 = node_map[(7, 4)]
    assert grid.neighbors(fs74, Direction.E) == [(((6, 4), '/'), Direction.N)]

    fs64 = node_map[(6, 4)]
    assert grid.neighbors(fs64, Direction.N) == [(((6, 5), '.'), Direction.E)]

    bs67 = node_map[(6, 7)]
    assert grid.neighbors(bs67, Direction.N) == [(((6, 6), '\\'),Direction.W)]

    bs66 = node_map[(6, 6)]
    assert grid.neighbors(bs66, Direction.W) == [(((5, 6), '.'),Direction.N)]
    # print(bs66)
    # print(grid.neighbors(bs67, Direction.W))

def test_next_pos():
    pos = (6, 6)
    npos, d = next_pos(pos, Direction.N)
    assert (npos, d) == ((5, 6), Direction.N)

if __name__ == '__main__':
    test_next_pos()
    test_neighbors()
    test_bfs()
