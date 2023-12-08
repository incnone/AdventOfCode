import textwrap
from collections import Counter
from enum import Enum


def get_test_input() -> str:
    return textwrap.dedent("""\
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return data


class CamelhandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OAK = 3
    FULL_HOUSE = 4
    FOUR_OAK = 5
    FIVE_OAK = 6


def find_handtype_from_items(items):
    if items[0][1] == 5:
        return CamelhandType.FIVE_OAK
    elif items[0][1] == 4:
        return CamelhandType.FOUR_OAK
    elif items[0][1] == 3:
        if items[1][1] == 2:
            return CamelhandType.FULL_HOUSE
        else:
            return CamelhandType.THREE_OAK
    elif items[0][1] == 2:
        if items[1][1] == 2:
            return CamelhandType.TWO_PAIR
        else:
            return CamelhandType.ONE_PAIR
    else:
        return CamelhandType.HIGH_CARD


class CamelHand(object):
    card2rank = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    @staticmethod
    def find_camelhand_type(s: str):
        c = Counter(s)
        items = c.most_common()
        return find_handtype_from_items(items)

    def __init__(self, s):
        self.hand, bid = s.split()
        self.bid = int(bid)
        self.hand_type = self.find_camelhand_type(self.hand)
        self.cards = tuple([self.hand_type.value] + [CamelHand.card2rank[c] for c in self.hand])

    def __lt__(self, other):
        return self.cards < other.cards

    def __eq__(self, other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(self.cards)

    def __repr__(self):
        return self.hand


class JokerHand(object):
    card2rank = {
        'J': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    @staticmethod
    def find_jokerhand_type(s: str):
        c = Counter(s)
        num_j = 0
        if 'J' in c:
            num_j = c['J']
            if num_j == 5:
                return CamelhandType.FIVE_OAK
            del c['J']
        items = c.most_common()
        items[0] = (items[0][0], items[0][1] + num_j)
        return find_handtype_from_items(items)

    def __init__(self, s):
        self.hand, bid = s.split()
        self.bid = int(bid)
        self.hand_type = self.find_jokerhand_type(self.hand)
        self.cards = tuple([self.hand_type.value] + [JokerHand.card2rank[c] for c in self.hand])

    def __lt__(self, other):
        return self.cards < other.cards

    def __eq__(self, other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(self.cards)

    def __repr__(self):
        return self.hand


def part_1(data):
    hands = []
    for s in data:
        hands.append(CamelHand(s))
    hands = sorted(hands)

    winnings = 0
    for offrank, card in enumerate(hands):
        rank = offrank + 1
        winnings += rank*card.bid
    print(f'Part 1: {winnings}')


def part_2(data):
    hands = []
    for s in data:
        hands.append(JokerHand(s))
    hands = sorted(hands)

    winnings = 0
    for offrank, card in enumerate(hands):
        rank = offrank + 1
        winnings += rank*card.bid
    print(f'Part 2: {winnings}')


def main():
    data = read_input(day_number=7, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
