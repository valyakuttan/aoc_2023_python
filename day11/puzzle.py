from collections import deque


def expand(universe):
    col_doubles = transpose(double_rows(transpose(universe)))
    return double_rows(col_doubles)


def double_rows(xss):
    xs = []
    for l in xss:
        if all(c == '.' for c in l):
            xs.append(l)
            xs.append(l)
        else:
            xs.append(l)
    return xs


def transpose(xs):
    return [''.join(x) for x in zip(*xs)]


def neighbors(x, y, rows, cols):
    xs = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
    return [(i, j) for i, j in xs if 0 <= i < rows and 0 <= j < cols]


def galaxy_locations(universe):
    return [(i, j) for i, xs in enumerate(universe) for j, c in enumerate(xs) if c == '#']


def bfs(positions, start, rows, cols):
    queue = deque([start])
    count = 0
    visited = set()
    xs = []
    while queue:
        level_count = len(queue)
        while level_count > 0:
            point = queue.pop()
            if point not in visited:
                visited.add(point)
                if point in positions:
                    xs.append((point, count))

            for x in neighbors(point[0], point[1], rows, cols):
                if x not in visited:
                    queue.appendleft(x)

            level_count -= 1

        count += 1

    return xs

def all_pairs(xs):
    xss = []
    while len(xs) > 1:
        xss.append((xs[0], xs[1:]))
        xs = xs[1:]
    return xss

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def mhd_list(p, lst):
    return sum(map(lambda q: manhattan_distance(p, q), lst))

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xs = list(data.split('\n'))
    exs = expand(xs)
    glocs = galaxy_locations(exs)
    pairs = all_pairs(glocs)
    distances = [mhd_list(p, lst) for p, lst in pairs]
    #print(distances)
    print(sum(distances))

if __name__ == '__main__':
    main()
