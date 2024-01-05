from puzzle import *

def test_mapper(mappings):
    m = get_mapper(mappings)
    xs = [0, 10, 49, 50, 51, 97, 98, 99, 100, 101, 150]
    expected = [0, 10, 49, 52, 53, 99, 50, 51, 100, 101, 150]

    ys = [m(x) for x in xs]

    assert ys == expected

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
    mappings = [get_mapper(m) for m in mappings]

    def seed2location(x):
        return mappings[6](
             mappings[5](
                mappings[4](
                    mappings[3](
                        mappings[2](
                            mappings[1](
                                mappings[0](x)
                    )   )   )
                )
            )
        )

    result = [seed2location(s) for s in SEEDS]
    result = min(result)
    assert result == 35

    SEEDS = [x for a, b in chunks(SEEDS, 2) for x in range(a, a + b)]
    #print(SEEDS)

    result = min(seed2location(s) for s in iter(SEEDS))
    assert result == 46


if __name__ == '__main__':
    test()
