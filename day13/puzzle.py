# --- Day 13: Point of Incidence ---

# With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

# There's just one problem: you don't see any lava.

# You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

# As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

# You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

# For example:

# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#

# To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

# In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

# 123456789
#     ><
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#     ><
# 123456789

# In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

# The second pattern reflects across a horizontal line instead:

# 1 #...##..# 1
# 2 #....#..# 2
# 3 ..##..### 3
# 4v#####.##.v4
# 5^#####.##.^5
# 6 ..##..### 6
# 7 #....#..# 7

# This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

# To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

# Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

from itertools import cycle, chain


def height(matrix):
    return len(matrix)


def width(matrix):
    return min(len(x) for x in matrix) if matrix else 0


def transpose(matrix):
    return ([''.join(x) for x in zip(*matrix)])


def to_str(matrix):
    xs = chain(*zip(matrix[: -1], cycle(['\n'])))
    return ''.join(chain(xs, [matrix[-1]]))


def vsymmetry_of(matrix):
    result = []
    w = width(matrix)
    for p in range(w - 1, 0, -1):
        if is_vsymmetric_about(matrix, p):
            result.append(p)

    p = max(result) if result else 0
    return p


def hsymmetry_of(matrix):
    return vsymmetry_of(transpose(matrix))


def symmetry(matrix, memo):
    h = mat_hash(matrix)
    if h in memo:
        return memo[h]

    s = hsymmetry_of(matrix), vsymmetry_of(matrix)
    memo[h] = s
    return memo[h]


def is_vsymmetric_about(matrix, pos):
    return all(is_symmetric(x, pos) for x in matrix)


def is_symmetric(xs, pos):
    """
        xs is symmetric about the line between pos - 1 and pos.
        So there are pos items to the left of line of symmetry.
    """

    left, right = xs[:pos], xs[pos:]
    return all(x == y for x, y in zip(right, left[::-1]))


def matrix_wtih_symbol_flipped(matrix, row, col):
    xs = matrix[row]
    s = '#' if xs[col] == '.' else '.'
    ys = xs[:col] + s + xs[col + 1:]

    return matrix[:row] + [ys] + matrix[row + 1:]


def corrected_symmetry(matrix):
    flipped_matrices = (matrix_wtih_symbol_flipped(matrix, r, c)
                        for r in range(height(matrix))
                        for c in range(width(matrix)))

    memo = {}
    hresult = []
    vresult = []

    for m in flipped_matrices:
        h, v = symmetry(m, memo)
        hresult.append(h)
        vresult.append(v)

    rh, rv = max(hresult) if hresult else 0, max(vresult) if vresult else 0
    return rh, rv


def mat_hash(matrix):
    return ''.join(matrix)


def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xs = data.split('\n\n')
    patterns = []
    for x in xs:
        patterns.append([s for s in x.split('\n') if s])

    # result = ((vsymmetry_of(m), hsymmetry_of(m)) for m in patterns)
    # symmetry_sum = sum(v + 100 * h for v, h in result)

    # for m in mats:
    #     v = m.find_vsym()
    #     h = m.find_hsym()
    #     result += v + 100 * h
    # assert symmetry_sum == 31877
    #

    result = map(lambda x: 100 * x[0] + x[1],
                 (corrected_symmetry(m) for m in patterns))
    val = sum(result)
    print(val)
    assert val != 65879


if __name__ == '__main__':
    main()
