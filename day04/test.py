from puzzle import *

def test():
    with open('sample.input', 'r') as file:
        data = file.read()

    lines = data.split('\n')
    cards = [parse_card(l) for l in lines]

    max_card_id = max(cards, key=lambda x: x[0])[0]

    counts = [numcards(c, cards, max_card_id) for c in cards]
    print(sum(counts))


if __name__ == '__main__':
    test()
