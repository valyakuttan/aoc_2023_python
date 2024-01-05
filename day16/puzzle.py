from queue import Queue
from squaregrid import SquareGrid, Node, Point, Direction
from typing import Dict, Optional, Tuple, NewType

ND = NewType('ND', Tuple[Node, Direction])


def breadth_first_search(
    graph: SquareGrid,
    start_node: Node,
    start_direction: Direction = Direction.E
) -> Dict[ND, Optional[ND]]:

    frontier: Queue[ND] = Queue()
    start_nd = ND((start_node, start_direction))
    frontier.put(start_nd)

    came_from: Dict[ND, Optional[ND]] = {}
    came_from[start_nd] = None
    count: int = 1
    while not frontier.empty():
        current_nd: ND = frontier.get()

        for next_tuple in graph.neighbors(current_nd[0], current_nd[1]):
            nd = ND(next_tuple)
            if nd not in came_from:
                frontier.put(nd)
                came_from[nd] = current_nd
                count += 1

    return came_from


def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xss = list(data.split('\n'))

    n = len(xss)
    node_map = {(i, j): ((i, j), c) for i, xs in enumerate(xss)
                for j, c in enumerate(xs)}

    grid = SquareGrid(n, n)
    grid.node_map = node_map

    start = node_map[(0,0)]
    m = breadth_first_search(grid, start, Direction.E)
    s = set(k[0] for k in m)
    energized_tiles = len(s)

    print(energized_tiles)

if __name__ == '__main__':
    main()
