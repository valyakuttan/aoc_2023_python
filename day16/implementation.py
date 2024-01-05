from typing import TypeVar, Protocol, List, Self, Tuple, Iterator
import collections

Node = TypeVar('Node')
T = TypeVar('T')


class Graph(Protocol):
    def neighbors(self: Self, node: Node) -> List[Node]: pass


class SimpleGraph(Graph):
    def __init__(self: Self):
        self.edges: dict[Node, List[Node]] = {}

    def neighbors(self: Self, node: Node) -> List[Node]:
        return self.edges[node]


class Queue:
    def __init__(self: Self):
        self.elements = collections.deque()

    def empty(self: Self) -> bool:
        return not self.elements

    def put(self: Self, x: T):
        self.elements.append(x)

    def get(self: Self) -> T:
        return self.elements.popleft()


GridLocation = Tuple[int, int]


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []

    def in_bounds(self, location: GridLocation) -> bool:
        (x, y) = location
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, location: GridLocation) -> bool:
        return location not in self.walls

    def neighbors(self, location: GridLocation) -> Iterator[GridLocation]:
        (x, y) = location
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results
