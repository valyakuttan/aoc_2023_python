from enum import Enum
from collections import deque

class Node:
    def __init__(self):
        self._node = None
        self._nodetype = None

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    @property
    def nodetype(self):
        return self._nodetype

    @nodetype.setter
    def nodetype(self, value):
        self._nodetype = value

    def __str__(self) -> str:
        return str(self._node)

    def __eq__(self, other: object) -> bool:
        return (
            self.__class__ == other.__class__ and
            self._node == other._node
        )

    def __hash__(self) -> int:
        return hash(self._node)


def new_node(node, nodetype):
    n = Node()
    n.node = node
    n.nodetype = nodetype
    return n


class NodeType(Enum):
    VER = 1
    HOR = 2
    LSH = 3
    JSH = 4
    FSH = 5
    SVN = 6


type_map = {
    '|': NodeType.VER,
    '-': NodeType.HOR,
    'L': NodeType.LSH,
    'J': NodeType.JSH,
    'F': NodeType.FSH,
    '7': NodeType.SVN,
}

matching_nodes = {
    NodeType.VER: {
        'N': [NodeType.VER, NodeType.FSH, NodeType.SVN],
        'S': [NodeType.LSH, NodeType.JSH],
        'E': [],
        'W': [],
    },
    NodeType.HOR: {
        'N': [],
        'S': [],
        'E': [NodeType.HOR, NodeType.JSH, NodeType.SVN],
        'W': [NodeType.LSH, NodeType.FSH],
    },

    NodeType.LSH:  {
        'N': [NodeType.FSH, NodeType.SVN],
        'S': [],
        'E': [NodeType.JSH, NodeType.SVN],
        'W': [],
    },

    NodeType.JSH:  {
        'N': [NodeType.FSH, NodeType.SVN],
        'S': [],
        'E': [],
        'W': [NodeType.FSH],
    },

    NodeType.FSH:  {
        'N': [],
        'S': [],
        'E': [NodeType.SVN],
        'W': [],
    },

    NodeType.SVN:  {
        'N': [],
        'S': [],
        'E': [],
        'W': [],
    },

}


def can_connect(node1, node2, direction):
    "Check whether node1 can connect node2 in the direction."
    comp_dirs = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}
    c1 = node1.nodetype in matching_nodes[node2.nodetype][direction]
    c2 = node2.nodetype in matching_nodes[node1.nodetype][comp_dirs[direction]]

    return c1 or c2


def neighbors(node, pos_to_nodes):
    def check_match(n, d):
        return can_connect(n, node, d)

    (x, y), _ = node.node
    node_type = node.nodetype

    ns = []
    if node_type == NodeType.VER:
        north, south = (x - 1, y), (x + 1, y)
        ns += matching_neighbors(
            [('N', north), ('S', south)],
            check_match,
            pos_to_nodes
        )
    elif node_type == NodeType.HOR:
        west, east = (x, y - 1), (x, y + 1)
        ns += matching_neighbors(
            [('W', west), ('E', east)],
            check_match,
            pos_to_nodes
        )
    elif node_type == NodeType.LSH:
        north, east = (x - 1, y), (x, y + 1)
        ns += matching_neighbors(
            [('N', north), ('E', east)],
            check_match,
            pos_to_nodes
        )
    elif node_type == NodeType.JSH:
        north, west = (x - 1, y), (x, y - 1)
        ns += matching_neighbors(
            [('N', north), ('W', west)],
            check_match,
            pos_to_nodes
        )
    elif node_type == NodeType.FSH:
        east, south = (x, y + 1), (x + 1, y)
        ns += matching_neighbors(
            [('E', east), ('S', south)],
            check_match,
            pos_to_nodes
        )

    elif node_type == NodeType.SVN:
        west, south = (x, y - 1), (x + 1, y)
        ns += matching_neighbors(
            [('W', west), ('S', south)],
            check_match,
            pos_to_nodes
        )

    return ns


def matching_neighbors(dir_pos_tuple_lst, check_match, pos_to_nodes):
    xs = []
    for d, p in dir_pos_tuple_lst:
        if p in pos_to_nodes and check_match(pos_to_nodes[p], d):
            xs.append(pos_to_nodes[p])

    return xs


def parse_input(data, start_nodetype):
    lines = data.split('\n')
    xs = (((r, c), ch) for (r, l) in enumerate(lines)
          for c, ch in enumerate(l))

    xs = filter(lambda node: node[1] in 'S|-LJF7', xs)

    nodes = []
    start_node = None
    for pos, ch in xs:
        if ch != 'S':
            value = (pos, ch)
            node_type = type_map[ch]
            nodes.append(new_node(value, node_type))
        else:
            value = (pos, ch)
            start_node = new_node(value, start_nodetype)
            nodes.append(start_node)

    return start_node, nodes

def bfs(graph, start):
    queue = deque([start])
    count = 0
    visited = set()
    xs = []
    while queue:
        level_count = len(queue)
        while level_count > 0:
            n = queue.pop()
            if n not in visited:
                visited.add(n)
                xs.append((n, count))

            for x in graph[n]:
                if x not in visited:
                    queue.appendleft(x)
            
            level_count -= 1

        count += 1

    return xs

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    start, nodes = parse_input(data, NodeType.VER)
    pos_to_nodes = {node.node[0]: node for node in nodes}

    kvs = ((n, neighbors(n, pos_to_nodes)) for n in nodes)
    graph = {k: v for k, v in kvs if len(v) == 2}

    vs = bfs(graph, start)
    max_distance = max(map(lambda x: x[1], vs))
    print(max_distance)

if __name__ == '__main__':
    main()
