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


class Matrix:

    def find_vsym(self):
        result = []
        w = self.width()

        for p in range(w - 1, 0, -1):
            if self.is_vsym_about(p):
                result.append(p)

        return max(result) if result else 0

    def find_hsym(self):
        return self.transpose().find_vsym()

    def is_vsym_about(self, pos):
        return all(is_symmetric(x, pos) for x in self.matrix)

    def transpose(self):
        return Matrix([''.join(x) for x in zip(*self.matrix)])

    def height(self):
        return len(self.matrix)

    def width(self):
        return len(self.matrix[0])

    def __init__(self, matrix):
        self.matrix = matrix[:]

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Matrix):
            return self.matrix == other.matrix
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(''.join(self.matrix))

    def __str__(self) -> str:
        xs = chain(*zip(self.matrix[: -1], cycle(['\n'])))
        return ''.join(chain(xs, [self.matrix[-1]]))


def is_symmetric(xs, pos):
    """
        xs is symmetric about the line between pos - 1 and pos.
        So there are pos items in the left.
    """

    left, right = xs[:pos], xs[pos:]
    return all(x == y for x, y in zip(right, left[::-1]))


def test_example_symmetry():
    xs = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]

    m1 = Matrix(xs)
    assert max(m1.find_vsym()) == 5


def test_symmetry():
    xs = "####..###"
    assert (is_symmetric(xs, 5))

    pattern = [
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

    m = Matrix(pattern)
    assert m.is_vsym_about(2)

    pos = 2
    assert (all(is_symmetric(x, pos) for x in pattern))


def test():
    test_example_symmetry()
    test_symmetry()


def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xs = data.split('\n\n')
    patterns = []
    for x in xs:
        patterns.append([s for s in x.split('\n') if s])

    mats = [Matrix(x) for x in patterns]

    result = 0
    for m in mats:
        v = m.find_vsym()
        h = m.find_hsym()
        result += v + 100 * h

    print("Result:", result)


if __name__ == '__main__':
    main()
