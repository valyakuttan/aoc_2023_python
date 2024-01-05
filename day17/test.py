from squaregrid import SquareGrid, Point
from puzzle import dijkstra_search


def test_sample():
    with open('sample.input', 'r') as file:
        data = file.read()

    xss = list(data.split('\n'))

    n = len(xss)
    point_to_cost = {Point(int(i), int(j)): int(c)
                     for i, xs in enumerate(xss) for j, c in enumerate(xs)}
    grid = SquareGrid(n, n, point_to_cost)

    start = Point(0, 0)
    goal = Point(n - 1, n - 1)
    c = dijkstra_search(grid, start, goal)

    assert min(v for k, v in c.items() if k.point == Point(0, 2)) == 5
    assert min(v for k, v in c.items() if k.point == Point(0, 3)) == 8
    assert min(v for k, v in c.items() if k.point == Point(0, 4)) == 14
    assert min(v for k, v in c.items() if k.point == Point(0, 5)) == 17
    assert min(v for k, v in c.items() if k.point == Point(0, 6)) == 23
    assert min(v for k, v in c.items() if k.point == Point(0, 8)) == 29
    assert min(v for k, v in c.items() if k.point == Point(2, 10)) == 43
    assert min(v for k, v in c.items() if k.point == goal) == 102
    print(min(v for k, v in c.items() if k.point == goal))

if __name__ == '__main__':
    test_sample()
