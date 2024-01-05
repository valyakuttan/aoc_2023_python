from puzzle import *


def test_expansion():
    with open('sample.input', 'r') as file:
        data = file.read()

    lines = list(data.split('\n'))
    rows, cols = len(lines), max(len(l) for l in lines)
    assert rows == 10
    assert cols == 10

    expanded = expand(lines)
    rows, cols = len(expanded), max(len(l) for l in expanded)
    assert rows == 12
    assert cols == 13


def test_neighbors():
    ns = neighbors(0, 0, 10, 12)
    assert ns == [(1, 0), (0, 1)]
    assert neighbors(1, 1, 10, 12) == [(0, 1), (2, 1), (1, 0), (1, 2)]
    assert neighbors(9, 11, 10, 12) == [(8, 11), (9, 10)]
    assert neighbors(8, 11, 10, 12) == [(7, 11), (9, 11), (8, 10)]

def test_galaxy_locations():
    u = ['...#......',
         '.......#..',
         '#.........',
         '..........',
         '......#...',
         '.#........',
         '.........#',
         '..........',
         '.......#..',
         '#...#.....']

    assert galaxy_locations(u) == [
        (0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
    
    eu = expand(u)
    xss = galaxy_locations(eu)
    yss = all_pairs(xss)
    
    sum_dist = sum(mhd_list(p, lst) for p, lst in yss)
    print(sum_dist)

def test():
    test_expansion()
    test_neighbors()
    test_galaxy_locations()


if __name__ == "__main__":
    test()
