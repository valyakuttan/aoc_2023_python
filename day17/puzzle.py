from typing import Dict, Tuple, List, cast

from squaregrid import SquareGrid, Point
from priorityqueue import PriorityQueue


class Node:
    point: Point
    last_three_points: List[Point] = []

    def __init__(self, point: Point, last_three_points: List[Point]) -> None:
        self.point = point
        self.last_three_points = last_three_points

    def __eq__(self, _other: object) -> bool:
        if self.__class__ == _other.__class__:
            other = cast(Node, _other)
            return self.to_tuple().__eq__(other.to_tuple())

        return False

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __lt__(self, other: 'Node'):
        return self.to_tuple() < other.to_tuple()

    def __repr__(self) -> str:
        return f' {str(self.point)} {self.last_three_points}'

    def to_tuple(self) -> Tuple[Point, ...]:
        xs = self.last_three_points + [self.point]
        return tuple(xs)


def new_node(p: Point, last_three_points: List[Point]) -> Node:
    return Node(p, last_three_points)


def dijkstra_search(graph: SquareGrid, start: Point, goal: Point) -> Dict[Node, int]:
    frontier: PriorityQueue[int, Node] = PriorityQueue()
    cost_so_far: Dict[Node, int] = {}

    start_node = new_node(start, [])
    frontier.put(start_node, 0)
    cost_so_far[start_node] = 0

    while not frontier.empty():

        current_node: Node = frontier.get()
        if current_node.point == goal:
            break

        nds = legal_neighbors(graph, current_node)
        for next_node in nds:
            new_cost = cost_so_far[current_node] + \
                edge_cost(graph, current_node, next_node)

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put(next_node, priority)

    return cost_so_far


def edge_cost(graph: SquareGrid, _src: Node, dst: Node) -> int:
    return graph.point_weight[dst.point]

neighbors: Dict[Node, List[Node]] = {}
def legal_neighbors(graph: SquareGrid, node: Node) -> List[Node]:
    if node in neighbors:
        return neighbors[node]

    back = dict(zip('NSEW', 'SNWE'))
    nds = []
    last_three_pts = node.last_three_points
    pt = node.point
    for n in graph.adjacent_points(pt):
        xs = last_three_pts[:] + [pt, n]
        ys = zip(xs, xs[1:])
        moves = list(map(lambda t: edge_to_direction(*t), ys))

        run_of_four = moves and moves.count(moves[0]) == 4
        going_back = len(moves) >= 2 and (
            back[moves[-1]] == moves[-2])

        if not run_of_four and not going_back:
            nd = new_node(n, last_three_pts[-2:] + [pt])
            nds.append(nd)

    neighbors[node] = nds
    return neighbors[node]


def edge_to_direction(src: Point, dst: Point) -> str:
    x1, y1 = src.to_tuple()
    x2, y2 = dst.to_tuple()
    if x1 == x2:
        return 'E' if y1 < y2 else 'W'
    if y1 == y2:
        return 'S' if x1 < x2 else 'N'
    return 'U'


def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xss = list(data.split('\n'))

    n = len(xss)
    point_to_cost = {Point(int(i), int(j)): int(c)
                     for i, xs in enumerate(xss) for j, c in enumerate(xs)}
    grid = SquareGrid(n, n, point_to_cost)

    start = Point(0, 0)
    goal = Point(n - 1, n - 1)
    c = dijkstra_search(grid, start, goal)

    print(min(v for k, v in c.items() if k.point == goal))


if __name__ == '__main__':
    main()
