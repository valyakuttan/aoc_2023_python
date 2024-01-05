from itertools import islice

from puzzle import *

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

matrix = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
        ]

def test_sample():
    with open('sample.input', 'r') as file:
        data = file.read()

    xs = data.split('\n\n')
    patterns = []
    for x in xs:
        patterns.append([s for s in x.split('\n') if s])

    result = ((vsymmetry_of(m), hsymmetry_of(m)) for m in patterns)
    symmetry_sum = sum(v + 100 * h for v, h in result)
    # print(symmetry_sum)
    assert symmetry_sum == 405


def test_symmetry():
    xs = "####..###"
    assert is_symmetric(xs, 5)

    m = [
        "#..#.....",
        ".##.##..#",
        "####..###",
        "#..###.##",
        "#..#.###.",
        "####.....",
        "....#..#.",
        "#####....",
        "#####....",
        "....#..#.",
        "####....#",
        "#..#.###.",
        "#..###.##",
    ]

    assert is_vsymmetric_about(m, 2)

    pos = 2
    assert (all(is_symmetric(x, pos) for x in m))


def test_example_symmetry():
    m = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]

    assert vsymmetry_of(m) == 5


def test_symbol_flip():
    m = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]

    m1 = matrix_wtih_symbol_flipped(m, 0, 0)
    # print(to_str(m))
    # print()
    # print()
    # print(to_str(m1))
    assert m1[0][0] == '.'

def test_alternate_symmetry():
    with open('sample.input', 'r') as file:
        data = file.read()

    xs = data.split('\n\n')
    
    patterns = []
    for x in xs:
        patterns.append([s for s in x.split('\n') if s])
    
    m = patterns[1]
    print(to_str(m))

    t, v = corrected_symmetry(m)
    print(t, v)

def test():
    test_example_symmetry()
    test_symmetry()
    test_sample()
    test_symbol_flip()
    test_alternate_symmetry()

if __name__ == '__main__':
    test()
