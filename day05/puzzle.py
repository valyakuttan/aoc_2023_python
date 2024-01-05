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

    mappings = [
        SEED_TO_SOIL,
        SOIL_TO_FERTILIZER,
        FERTILIZER_TO_WATER,
        WATER_TO_LIGHT,
        LIGHT_TO_TEMPERATURE,
        TEMPERATURE_TO_HUMIDITY,
        HUMIDITY_TO_LOCATION,
    ]
    mappings = [get_mapper(m) for m in mappings]

    def seed2location(x):
        return mappings[6](
            mappings[5](
                mappings[4](
                    mappings[3](
                        mappings[2](
                            mappings[1](
                                mappings[0](x)
                            )))
                )
            )
        )

    result = [seed2location(s) for s in SEEDS]
    result = min(result)
    assert result > 294198454
    assert result == 535088217

    SEEDS = [x for a, b in chunks(SEEDS, 2) for x in range(a, a + b)]
    #print(SEEDS)

    #result = min(seed2location(s) for s in iter(SEEDS))
    print(result)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield tuple(lst[i:i + n])

def get_mapper(xs):
    mappings = []
    for x in xs:
        dst, src, rng, *_ = x
        mappings.append((src, src + rng, dst))

    mappings.sort(key=lambda x: x[0])

    memo = {}

    def f(x):
        if x in memo:
            return memo[x]

        v = None
        for lo, hi, dst in mappings:
            if lo <= x < hi:
                v = dst + x - lo
                break

        memo[x] = v if v else x
        return memo[x]

    return f


def parse_map(s):
    s = s.split(':')[1].strip()
    s = s.split('\n')
    return [[int(y) for y in x.split(' ') if y] for x in s]


if __name__ == '__main__':
    main()
