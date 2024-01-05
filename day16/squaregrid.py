from typing import Tuple, List, Dict, NewType, TypeVar
from enum import Enum


class Direction(Enum):
    N = 0
    S = 1
    E = 2
    W = 3


Point = NewType('Point', Tuple[int, int])
Node = NewType('Node', Tuple[Point, str])


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.node_map: Dict[Point, Node] = {}

    def in_bounds(self, location: Point) -> bool:
        (x, y) = location
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, node: Node, direction: Direction) -> List[Tuple[Node, Direction]]:
        pos, ch = node
        ns: List[Tuple[Point, Direction]] = []

        if ch == '.':
            ns = [next_pos(pos, direction)]

        if ch == '|':
            if direction in [Direction.E, Direction.W]:
                ns = [next_pos(pos, Direction.S), next_pos(pos, Direction.N)]
            else:
                ns = [next_pos(pos, direction)]

        if ch == '-':
            if direction in [Direction.N, Direction.S]:
                ns = [next_pos(pos, Direction.E), next_pos(pos, Direction.W)]
            else:
                ns = [next_pos(pos, direction)]

        if ch == '/':
            if direction == Direction.N:
                ns = [next_pos(pos, Direction.E)]
            elif direction == Direction.S:
                ns = [next_pos(pos, Direction.W)]
            elif direction == Direction.E:
                ns = [next_pos(pos, Direction.N)]
            else:
                ns = [next_pos(pos, Direction.S)]

        if ch == '\\':
            if direction == Direction.N:
                ns = [next_pos(pos, Direction.W)]
            elif direction == Direction.S:
                ns = [next_pos(pos, Direction.E)]
            elif direction == Direction.E:
                ns = [next_pos(pos, Direction.S)]
            else:
                ns = [next_pos(pos, Direction.N)]

        return [(self.node_map[p], d)
                for p, d in filter(lambda t: self.in_bounds(t[0]), ns)]


T = TypeVar('T')


def reconstruct_path(came_from: dict[T, T],
                     start: T, goal: T) -> list[T]:

    current: T = goal
    path: list[T] = []
    if goal not in came_from:  # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def next_pos(pos: Point, direction: Direction) -> Tuple[Point, Direction]:
    x, y = pos
    if direction == Direction.N:
        return (Point((x - 1, y)), direction)
    if direction == Direction.S:
        return (Point((x + 1, y)), direction)
    if direction == Direction.E:
        return (Point((x, y + 1)), direction)
    if direction == Direction.W:
        return (Point((x, y - 1)), direction)
