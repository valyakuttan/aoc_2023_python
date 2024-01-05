from itertools import groupby

def load(xs):
    l = len(xs)
    return [x.count('O') * (l - i) for i, x in enumerate(xs)]

def tilt(line: str):
    xs = line.split('#')
    return '#'.join(''.join(sorted(x, reverse=True)) for x in xs)

def transpose(xs):
    return [''.join(x) for x in zip(*xs)]

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xs = list(data.split('\n'))
    xs = transpose([tilt(x) for x in transpose(xs)])
    ls = load(xs)
    print("load: ", sum(ls))

if __name__ == '__main__':
    main()
