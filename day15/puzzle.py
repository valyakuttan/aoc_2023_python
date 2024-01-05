from functools import reduce

def hash_value(s: str):
    return reduce(lambda a, c: (a + ord(c)) * 17 % 256, s, 0)

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    xs = list(data.split('\n'))[0]
    hashes = [hash_value(x) for x in xs.split(',')]
    print(sum(hashes))
if __name__ == '__main__':
    main()
