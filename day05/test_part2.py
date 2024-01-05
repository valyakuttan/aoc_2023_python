import functools
from functools import reduce

from part2 import *


def test_mapper():
    SEED_TO_SOIL = [[50, 98, 2], [52, 50, 48]]
    m1 = get_mapper(SEED_TO_SOIL)
    seeds = [(55, 13), (79, 14)]
    result = m1(seeds)
    assert result == [(57, 13), (81, 14)]

    assert m1([(0, 49)]) == [(0, 49)]
    assert m1([(20, 40)]) == [(20, 30), (52, 10)]
    assert m1([(50, 40)]) == [(52, 40)]
    assert m1([(100, 40)]) == [(100, 40)]
    assert m1([(98, 40)]) == [(50, 2), (100, 38)]
    assert m1([(41, 80)]) == [(41, 9), (52, 48), (50, 2), (100, 21)]


def test():
    with open('sample.input', 'r') as file:
        data = file.read()

    xs = data.split('\n\n')

    SEEDS = xs[0].split(':')
    SEEDS = [int(x.strip()) for x in SEEDS[1].split(' ') if x]

    SEED_TO_SOIL = parse_map(xs[1])
    SOIL_TO_FERTILIZER = parse_map(xs[2])
    FERTILIZER_TO_WATER = parse_map(xs[3])
    WATER_TO_LIGHT = parse_map(xs[4])
    LIGHT_TO_TEMPERATURE = parse_map(xs[5])
    TEMPERATURE_TO_HUMIDITY = parse_map(xs[6])
    HUMIDITY_TO_LOCATION = parse_map(xs[7])

    mappings = [
        SEED_TO_SOIL,
        SOIL_TO_FERTILIZER,
        FERTILIZER_TO_WATER,
        WATER_TO_LIGHT,
        LIGHT_TO_TEMPERATURE,
        TEMPERATURE_TO_HUMIDITY,
        HUMIDITY_TO_LOCATION,
    ]

    # test_mapper(get_mapper(SEED_TO_SOIL))

    mappers = [get_mapper(m) for m in mappings]

    seeds = list(c for c in chunks(SEEDS, 2))
    # print("seeds: ", seeds) # [(79, 14), (55, 13)]
    m0 = mappers[0]
    # print("seed to soil map: ", SEED_TO_SOIL)
    result = m0(seeds)
    assert result == [(81, 14), (57, 13)]

    m1 = mappers[1]
    result = m1(result)
    assert result == [(81, 14), (57, 13)]

    m2 = mappers[2]
    result = m2(result)
    assert result == [(81, 14), (53, 4), (61, 9)]

    m3 = mappers[3]
    result = m3(result)
    assert result == [(74, 14), (46, 4), (54, 9)]

    m4 = mappers[4]
    result = m4(result)
    assert result == [(78, 3), (45, 11), (82, 4), (90, 9)]

    m5 = mappers[5]
    result = m5(result)
    assert result == [(78, 3), (46, 11), (82, 4), (90, 9)]

    m6 = mappers[6]
    result = m6(result)
    assert result == [(82, 3), (46, 10), (60, 1),
                      (86, 4), (94, 3), (56, 4), (97, 2)]

    seeds2location = reduce(compose2, mappers[::-1])
    assert seeds2location(seeds) == [(82, 3), (46, 10), (60, 1),
                                     (86, 4), (94, 3), (56, 4), (97, 2)]

    assert min(seeds2location(seeds), key=lambda x: x[0])[0] == 46

if __name__ == '__main__':
    test_mapper()
    test()
