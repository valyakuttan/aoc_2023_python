import functools

def main():
    with open('puzzle.input', 'r') as file:
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

    mappers = [
        SEED_TO_SOIL,
        SOIL_TO_FERTILIZER,
        FERTILIZER_TO_WATER,
        WATER_TO_LIGHT,
        LIGHT_TO_TEMPERATURE,
        TEMPERATURE_TO_HUMIDITY,
        HUMIDITY_TO_LOCATION,
    ]

    mappers = [get_mapper(m) for m in mappers]
    seeds2location = functools.reduce(compose2, mappers[::-1])
    seeds = list(c for c in chunks(SEEDS, 2))

    min_location = min(seeds2location(seeds), key=lambda x: x[0])[0]
    print(min_location)
    assert min_location == 51399228

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])

def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))

def get_mapper(xs):
    mappings = []
    for x in xs:
        mappings.append(tuple(x))

    mappings.sort(key=lambda x: x[1])

    return lambda rv: range_mapper_list(rv, mappings)

def range_mapper_list(range_value_lst, mappings):
    result = []
    for range_value in range_value_lst:
        result = range_mapper(range_value, mappings, result)

    return result

def range_mapper(range_value, mappings, result):
    # range_vale is of the form (lo, range) which is equivalent to
    # the mathematical half opn interval [lo, lo + range).
    #
    # mappings are of the form (destination, source, range) which
    # corresponds to the mapping from
    # [source, source + range) => [destination, destination + range)
    #
    if not mappings:
        return result + [range_value]

    lo, cnt = range_value
    hi = lo + cnt - 1

    (dst, left, count), *rest_mappings = mappings
    right = left + count - 1

    if hi < left:
        return result + [range_value]

    if lo < left and hi <= right:
        c1 = left - lo
        rng1 = (lo, c1)
        rng2 = (dst, cnt - c1)
        return result + [rng1, rng2]

    if lo < left and right < hi:
        c1 = left - lo
        rng1 = (lo, c1)

        c2 = right - left + 1
        rng2 = (dst, c2)

        rng3 = (right + 1, cnt - c1 - c2)
        result = result + [rng1, rng2]
        return range_mapper(rng3, rest_mappings, result)

    if left <= lo and hi <= right:
        dst_lo = dst + lo - left
        return result + [(dst_lo, cnt)]

    if lo <= right < hi:
        dst_lo = dst + lo - left
        c1 = right - lo + 1
        rng1 = (dst_lo, c1)
        next_range_value = (right + 1, cnt - c1)
        result = result + [rng1]
        return range_mapper(next_range_value, rest_mappings, result)

    if right < lo:
        return range_mapper(range_value, rest_mappings, result)


def parse_map(s):
    s = s.split(':')[1].strip()
    s = s.split('\n')
    return [[int(y) for y in x.split(' ') if y] for x in s]


if __name__ == '__main__':
    main()
