def parse_card(line):
    xs = line.split(':')
    id_part = list(filter(lambda x: x, xs[0].split(' ')))
    card_id = int(id_part[1])
    xs = xs[1].split('|')
    winning_numbers = [int(n) for n in xs[0].split(' ')if n]
    card_numbers = [int(n) for n in xs[1].split(' ')if n]

    return (card_id, winning_numbers, card_numbers)

memo = {}
def numcards(c, cards, max_card_id):
    card_id = c[0]
    if card_id in memo:
        return memo[card_id]
    winning = set(c[1])
    numbers = set(c[2])
    count = len(winning.intersection(numbers))

    if not count or card_id >= max_card_id:
        memo[card_id] = 1
        return memo[card_id]

    next_cards = (cards[x-1] for x in range(card_id + 1, card_id + count + 1) if x <= max_card_id)
    n = 1 + sum(numcards(c, cards, max_card_id) for c in next_cards)

    memo[card_id] = n
    return memo[card_id]

def main():
    with open('puzzle.input', 'r') as file:
        data = file.read()

    lines = filter(lambda x: x, data.split('\n'))
    cards = [parse_card(l) for l in lines]

    max_card_id = max(cards, key=lambda x: x[0])[0]

    n = sum(numcards(c, cards, max_card_id) for c in cards)
    print(n)
    assert n == 5667240

if __name__ == '__main__':
    main()
