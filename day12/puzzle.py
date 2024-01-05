# --- Day 12: Hot Springs ---

# You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.

# As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.

# "Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

# You look in the direction the researcher is pointing and suddenly notice the massive metal helixes towering overhead. "This way!"

# It only takes you a few more steps to reach the main gate of the massive fenced-off area containing the springs. You go through the gate and into a small administrative building.

# "Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

# "Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not until we get more lava to heat our forges. And our springs. The springs aren't very springy unless they're hot!"

# "Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal operation, but we should be able to find one springy enough to launch you up there!"

# There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.

# In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

# However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

# So, condition records with no unknown spring conditions might look like this:

# #.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1

# However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1

# Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

# In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

# The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

# The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

# ?###???????? 3,2,1
# .###.##.#...
# .###.##..#..
# .###.##...#.
# .###.##....#
# .###..##.#..
# .###..##..#.
# .###..##...#
# .###...##.#.
# .###...##..#
# .###....##.#

# In this example, the number of possible arrangements for each row is:

#     ???.### 1,1,3 - 1 arrangement
#     .??..??...?##. 1,1,3 - 4 arrangements
#     ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
#     ????.#...#... 4,1,1 - 1 arrangement
#     ????.######..#####. 1,6,5 - 4 arrangements
#     ?###???????? 3,2,1 - 10 arrangements

# Adding all of the possible arrangement counts together produces a total of 21 arrangements.

# For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?

from itertools import groupby, permutations

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read().splitlines()
    
    # data = [
    #     "???.### 1,1,3",
    #     ".??..??...?##. 1,1,3",
    #     "?#?#?#?#?#?#?#? 1,3,1,6",
    #     "????.#...#... 4,1,1",
    #     "????.######..#####. 1,6,5",
    #     "?###???????? 3,2,1",
    #     "?.#?#????###?#????? 1,1,11,1",
    #     ]


    result = [3, 1, 4, 3, 2, 1, 4, 2, 2, 10, 2, 2, 11, 6, 6, 7, 6, 2, 8, 1, 2, 3, 2, 9, 9,
              2, 1, 15, 21, 1, 7, 25, 1, 7, 4, 2, 8, 9, 4, 4, 3, 1, 1, 9, 2, 3, 3, 3, 4, 9,
              1, 3, 4, 3, 1, 2, 5, 2, 10, 3, 15, 16, 4, 12, 5, 2, 3, 4, 4, 2, 4, 20, 1, 1,
              2, 13, 1, 4, 3, 6, 3, 22, 7, 4, 2, 1, 1, 2, 6, 9, 4, 1, 2, 2, 9, 10, 12, 2, 13,
              2, 2, 23, 4, 1, 3, 4, 2, 6, 4, 13, 25, 13, 11, 2, 3, 12, 4, 16, 1, 6, 5, 3, 3,
              1, 7, 2, 2, 2, 1, 4, 17, 5, 3, 2, 4, 1, 14, 8, 1, 4, 2, 31, 4, 16, 12, 102, 7,
              1, 28, 1, 21, 1, 5, 2, 3, 1, 4, 2, 4, 4, 1, 12, 2, 2, 18, 4, 12, 4, 6, 6, 4,
              10, 1, 4, 3, 4, 2, 2, 12, 7, 1, 1, 1, 5, 1, 2, 12, 2, 24, 7, 2, 2, 1, 8, 3, 1,
              3, 4, 3, 20, 2, 2, 4, 2, 7, 2, 1, 12, 17, 11, 3, 4, 16, 14, 6, 1, 20, 11, 10,
              3, 6, 1, 7, 3, 9, 3, 2, 5, 6, 3, 26, 6, 6, 15, 2, 6, 5, 1, 4, 3, 1, 4, 6, 2, 6,
              3, 2, 31, 10, 11, 4, 2, 1, 1, 3, 6, 2, 21, 35, 4, 3, 2, 16, 6, 2, 3, 7, 3, 4, 15,
              4, 2, 10, 9, 13, 3, 1, 14, 25, 4, 1, 2, 6, 2, 9, 12, 6, 6, 4, 2, 1, 3, 3, 3, 6, 1,
              2, 3, 8, 3, 8, 20, 6, 2, 6, 4, 2, 4, 3, 4, 21, 4, 1, 4, 4, 1, 2, 1, 2, 26, 2, 4, 1,
              7, 3, 1, 1, 4, 3, 16, 8, 5, 4, 4, 2, 1, 9, 1, 5, 3, 5, 6, 4, 2, 2, 10, 2, 2, 17, 1,
              3, 3, 21, 1, 2, 3, 1, 4, 9, 1, 15, 1, 2, 4, 4, 8, 7, 2, 4, 1, 11, 29, 4, 21, 1, 3, 2,
              1, 2, 4, 1, 1, 2, 12, 4, 7, 4, 3, 2, 6, 6, 12, 1, 4, 3, 21, 3, 10, 2, 2, 4, 2, 11, 6,
              1, 3, 2, 8, 6, 1, 33, 3, 3, 10, 2, 2, 6, 10, 5, 4, 1, 3, 2, 25, 2, 8, 2, 2, 1, 3, 25,
              60, 2, 1, 6, 6, 7, 11, 6, 4, 1, 4, 1, 2, 12, 7, 3, 3, 6, 3, 2, 4, 5, 1, 11, 4, 3, 7,
              4, 1, 2, 11, 6, 5, 15, 4, 8, 2, 8, 4, 1, 12, 1, 6, 3, 9, 22, 7, 4, 3, 15, 2, 4, 9, 7,
              50, 5, 61, 2, 3, 4, 19, 2, 14, 6, 2, 18, 5, 1, 10, 2, 8, 2, 3, 2, 2, 1, 3, 10, 1, 1,
              3, 4, 35, 2, 7, 8, 3, 2, 2, 12, 2, 2, 9, 140, 8, 18, 3, 4, 2, 13, 3, 3, 4, 6, 4, 3, 20,
              7, 2, 18, 26, 2, 75, 1, 18, 4, 1, 6, 2, 1, 4, 2, 12, 3, 2, 4, 1, 1, 4, 7, 4, 5, 1, 2, 19,
              3, 1, 2, 4, 10, 2, 2, 1, 9, 3, 3, 6, 2, 9, 29, 4, 1, 12, 8, 7, 1, 4, 1, 1, 1, 4, 5, 5, 4,
              2, 40, 7, 4, 15, 4, 4, 9, 9, 4, 5, 2, 16, 3, 2, 3, 2, 1, 7, 2, 2, 5, 15, 1, 16, 3, 6, 1, 20,
              22, 3, 4, 3, 2, 6, 4, 1, 6, 3, 2, 7, 6, 1, 2, 1, 3, 3, 2, 5, 30, 20, 4, 2, 2, 4, 4, 4, 4, 3,
              1, 6, 5, 6, 3, 2, 41, 1, 36, 2, 2, 4, 3, 7, 3, 18, 3, 2, 4, 7, 15, 3, 6, 13, 2, 2, 3, 1, 6, 4,
              2, 7, 4, 1, 6, 2, 4, 5, 4, 6, 23, 1, 3, 17, 1, 4, 2, 35, 13, 31, 8, 5, 1, 1, 2, 2, 3, 7, 2, 1,
              6, 26, 8, 4, 1, 6, 4, 12, 2, 4, 13, 6, 4, 16, 11, 6, 2, 2, 3, 2, 8, 7, 4, 2, 1, 7, 2, 4, 7, 5,
              1, 2, 2, 6, 4, 7, 7, 1, 11, 15, 5, 10, 2, 3, 1, 7, 2, 5, 9, 2, 4, 2, 1, 4, 4, 1, 2, 17, 2, 2, 8,
              6, 4, 6, 2, 12, 58, 10, 4, 4, 2, 4, 3, 3, 4, 1, 2, 1, 3, 5, 3, 8, 1, 2, 20, 2, 7, 1, 2, 7, 4, 1,
              3, 12, 3, 14, 30, 5, 8, 1, 2, 4, 32, 6, 1, 35, 6, 8, 7, 36, 3, 3, 1, 1, 1, 2, 2, 2, 2, 2, 2, 28,
              9, 16, 2, 7, 3, 3, 10, 13, 35, 2, 1, 2, 35, 1, 9, 4, 6, 2, 2, 7, 5, 3, 2, 3, 11, 6, 3, 1, 4, 3, 18,
              18, 9, 4, 3, 2, 3, 8, 3, 11, 3, 6, 1, 3, 1, 1, 7, 3, 1, 4, 6, 10, 2, 2, 4, 3, 1, 3, 6, 2, 10, 2, 1, 2,
              38, 4, 8, 6, 1, 8, 12, 16, 2, 3, 23, 1, 2, 2, 1, 4, 4, 11, 3, 7, 6, 2, 4, 2, 3, 4, 2, 4, 1, 1, 23, 4,
              12, 1, 2, 6, 2, 5, 1, 4, 6, 2, 4, 1, 26, 24, 2, 3, 11, 3, 6, 1, 3, 4, 29, 2, 2, 2, 6, 2, 4, 1, 1, 22,
              6, 2, 2, 12, 8, 3, 6, 2, 22, 7, 2, 5, 2, 11, 1, 4, 5, 6, 3, 3, 7, 3, 7, 3, 2, 35, 4, 6, 2, 4, 3, 2, 1,
              7, 3, 5]                  

    assert(len(data) == len(result))
    print(sum(result))
    # data = data[1000: 1100]
    # counts = compute_chunk(data, 20, compute_arrangements)
    # print(counts)

def compute_chunk(data, chunksize, compute):
    start, end = 0, chunksize
    xs = data[start: end]
    result = []
    while xs:
        result += compute(xs)
        start, end = end, end + chunksize
        xs = data[start: end]
    
    return result

def compute_arrangements(xs):
    counts = []
    for x in xs:
        record, sizes = x.split(' ')
        sizes = [int(n) for n in sizes.split(',') if n]
        n = len(list(filter(lambda x: damaged_groups(x) == sizes, possible_arrangements(record))))
        counts.append(n)
    
    return counts

def positions_of(c, s):
    return (p for (p, x) in enumerate(s) if x == c)

def possible_arrangements(s):
    ps = positions_of('?', s)
    result = [s]
    for p in positions_of('?', s):
        result = [r for x in result for r in replace_char_at(p, '.#', x)]

    return iter(result)

def replace_char_at(pos, cs, s):
    prefix, suffix = s[:pos], s[pos+1:]
    return (''.join([prefix, c, suffix]) for c in cs)

def damaged_groups(xs):
    return [len(list(g)) for (k, g) in groupby(xs) if k != '.']

if __name__ == '__main__':
    main()
