import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


class Card(object):
    def __init__(self, s):
        cardno, nums = s.split(':')
        self.card_idx = int(cardno.split()[-1])
        winning_numbers, card_numbers = nums.split('|')
        self.winning_numbers = [int(x) for x in winning_numbers.split()]
        self.card_numbers = [int(x) for x in card_numbers.split()]

    def value(self):
        num_matches = self.num_winners()
        return 2**(num_matches - 1) if num_matches != 0 else 0

    def num_winners(self):
        num_matches = 0
        for num in self.winning_numbers:
            if num in self.card_numbers:
                num_matches += 1
        return num_matches


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(Card(line))
    return data


def part_1(data):
    print(f'Part 1: {sum(c.value() for c in data)}')


def part_2(data):
    cards = dict()
    copies = dict()
    min_idx = 1
    max_idx = 0
    for card in data:
        cards[card.card_idx] = card
        copies[card.card_idx] = 1
        max_idx = max(card.card_idx, max_idx)

    for card_idx in range(min_idx, max_idx+1):
        card = cards[card_idx]
        num_winners = card.num_winners()
        if num_winners > 0:
            for idx in range(card_idx + 1, card_idx + 1 + num_winners):
                copies[idx] += copies[card_idx]

    print(f'Part 2: {sum(copies.values())}')


def main():
    data = read_input(day_number=4, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
