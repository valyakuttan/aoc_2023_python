from puzzle import *


def test_tilt():
    xs = 'OO..O.##..OO..###O....O#'
    assert tilt(xs) == 'OOO...##OO....###OO....#'

    xs = 'OOOOO##....###....OOO#'
    assert tilt(xs) == 'OOOOO##....###OOO....#'

    xs = '##OO..O.##..OO..###O....O#'
    assert tilt(xs) == '##OOO...##OO....###OO....#'

    xs = '......#OO..O.##..OO..###O....O#'
    assert tilt(xs) == '......#OOO...##OO....###OO....#'


def test_sample():
    with open('sample.input', 'r') as file:
        data = file.read()
    
    xs = list(data.split('\n'))
    xs = transpose([tilt(x) for x in transpose(xs)])
    ls = load(xs)
    assert sum(ls) == 136

if __name__ == '__main__':
    test_tilt()
    test_sample()
