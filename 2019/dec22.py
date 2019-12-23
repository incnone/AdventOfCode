from enum import Enum
from typing import List
import textwrap
from util import modinv
import unittest


class InstrType(Enum):
    REVERSE = 0
    SIFT = 1
    CUT = 2


class ShuffleInstruction(object):
    def __init__(self, s):
        words = s.split()
        if words[1] == 'into':
            self.instr_type = InstrType.REVERSE
            self.param = 0
        elif words[1] == 'with':
            self.instr_type = InstrType.SIFT
            self.param = int(words[3])
        elif words[0] == 'cut':
            self.instr_type = InstrType.CUT
            self.param = int(words[1])

    def execute(self, cards):
        if self.instr_type == InstrType.REVERSE:
            return self.reverse(cards)
        elif self.instr_type == InstrType.SIFT:
            return self.sift(cards, self.param)
        elif self.instr_type == InstrType.CUT:
            return self.cut_n_cards(cards, self.param)

    @staticmethod
    def reverse(cards):
        return list(reversed(cards))

    @staticmethod
    def cut_n_cards(cards, n):
        return list(cards[n:] + cards[:n])

    @staticmethod
    def sift(cards, n):
        new_cards = [None]*len(cards)
        for idx, card in enumerate(cards):
            new_cards[n*idx % len(cards)] = card
        return new_cards


class DeckPermutation(object):
    @staticmethod
    def get_from_shuffle_instrs(deck_size, shuffle_instrs):
        deck_perm = DeckPermutation(deck_size)
        for instr in shuffle_instrs:
            deck_perm.multiply_by(instr)
        return deck_perm

    """A permutation of an abstract deck. Operations are applied: Reverse, then Sift, then Cut."""
    def __init__(self, deck_size):
        self.deck_size = deck_size
        self.reverse = False
        self.sift = 1
        self.cut = 0

    def __str__(self):
        if self.reverse:
            return '(r, s{}, c{})'.format(self.sift, self.cut)
        else:
            return '(s{}, c{})'.format(self.sift, self.cut)

    def __repr__(self):
        return '{}[{}]'.format(str(self), self.deck_size)

    def __eq__(self, other):
        return self.deck_size == other.deck_size \
               and self.reverse == other.reverse \
               and self.sift == other.sift \
               and self.cut == other.cut

    def __ne__(self, other):
        return not (self == other)

    def inverse_at(self, val):
        # Invert cut
        val = (val + self.cut) % self.deck_size

        # Invert sift
        val = (modinv(self.sift, self.deck_size)*val) % self.deck_size

        # Invert reverse
        if self.reverse:
            val = (self.deck_size - 1 - val) % self.deck_size
        return val

    def power(self, p):
        to_the_p = DeckPermutation(self.deck_size)
        to_the_p.reverse = self.reverse if p % 2 == 1 else False
        sift_power = pow(self.sift, p-1, self.deck_size)
        to_the_p.sift = (sift_power*self.sift) % self.deck_size     # self.sift**p

        if self.reverse:
            if p % 2 == 1:
                geo_sum = (1-sift_power)*modinv(1-self.sift**2, self.deck_size) if self.sift != 1 else (p-1)//2
                to_the_p.cut = (self.cut*sift_power + (self.cut + self.sift)*(1 - self.sift)*geo_sum) % self.deck_size
            elif p % 2 == 0:
                sift_power = (sift_power*self.sift) % self.deck_size     # self.sift**p
                geo_sum = (1-sift_power)*modinv(1-self.sift**2, self.deck_size) if self.sift != 1 else p//2
                to_the_p.cut = (((1 - self.sift - self.cut)*self.sift + self.cut)*geo_sum) % self.deck_size
        else:
            sift_power = (sift_power*self.sift) % self.deck_size     # self.sift**p
            to_the_p.cut = self.cut*((1-sift_power)//(1-self.sift)) % self.deck_size

        return to_the_p

    def multiply_by(self, shuffle_instr: ShuffleInstruction):
        # (cut n)*(sift m) = (sift m)*(cut m*n)
        # (reverse)*(cut n) = (cut -n)*(reverse)
        # (sift m)*(reverse) = (reverse)*(sift m)*(cut 1-m)
        # (cut n)*(cut m) = (cut n+m)
        # (reverse)*(reverse) = id
        # (sift m)*(sift n) = (sift m*n)
        if shuffle_instr.instr_type == InstrType.CUT:
            self.cut += shuffle_instr.param
        elif shuffle_instr.instr_type == InstrType.SIFT:
            self.cut = self.cut*shuffle_instr.param
            self.sift = self.sift*shuffle_instr.param
        elif shuffle_instr.instr_type == InstrType.REVERSE:
            self.cut = -self.cut + 1 - self.sift
            self.reverse = not self.reverse
        self.cut %= self.deck_size
        self.sift %= self.deck_size

    def multiply_by_perm(self, other):
        new_perm = DeckPermutation(self.deck_size)
        if other.reverse:
            new_perm.reverse = not self.reverse
            new_perm.sift = (self.sift*other.sift) % self.deck_size
            new_perm.cut = ((1 - self.sift - self.cut)*other.sift + other.cut) % self.deck_size
        else:
            new_perm.reverse = self.reverse
            new_perm.sift = (self.sift*other.sift) % self.deck_size
            new_perm.cut = (self.cut*other.sift + other.cut) % self.deck_size
        return new_perm

    def execute(self, cards):
        if self.reverse:
            cards = ShuffleInstruction.reverse(cards)
        cards = ShuffleInstruction.sift(cards, self.sift)
        cards = ShuffleInstruction.cut_n_cards(cards, self.cut)
        return cards


def parse_input(s):
    instrs = []
    for line in s.splitlines(keepends=False):
        instrs.append(ShuffleInstruction(line))

    return instrs


def part_1(shuffle_instrs):
    deck_perm = DeckPermutation(10007)
    for instr in shuffle_instrs:
        deck_perm.multiply_by(instr)

    cards = deck_perm.execute(list(range(deck_perm.deck_size)))
    return cards.index(2019)


def part_2(shuffle_instrs):
    return get_card_at_idx(
        idx=2020,
        shuffle_instrs=shuffle_instrs,
        num_cards=119315717514047,
        perm_power=101741582076661
    )


def get_card_at_idx(idx, shuffle_instrs, num_cards, perm_power):
    deck_perm = DeckPermutation.get_from_shuffle_instrs(deck_size=num_cards, shuffle_instrs=shuffle_instrs)
    return deck_perm.power(perm_power).inverse_at(idx)


class TestDeckPermutation(unittest.TestCase):
    def setUp(self) -> None:
        self.deck_size = None
        self.shuffle_instrs = None
        self.deck_perm = None

    def test_input_1(self):
        self._set_up(textwrap.dedent("""\
        deal with increment 7
        deal into new stack
        deal into new stack"""))
        self._all_tests()

    def test_input_2(self):
        self._set_up(textwrap.dedent("""\
        cut 6
        deal into new stack"""))
        self._all_tests()

    def test_input_3(self):
        self._set_up(textwrap.dedent("""\
        cut 6
        deal with increment 7
        deal into new stack"""))
        self._all_tests()

    def test_input_4(self):
        self._set_up(textwrap.dedent("""\
        deal with increment 3
        cut 2"""))
        self._all_tests()

    def test_input_5(self):
        self._set_up(textwrap.dedent("""\
        deal into new stack
        cut -2
        deal with increment 7
        cut 8
        cut -4
        deal with increment 7
        cut 3
        deal with increment 9
        deal with increment 3
        cut -1"""))
        self._all_tests()

    def test_file(self):
        with open('input/dec22.txt', 'r') as file:
            file_str = file.read()
        self._set_up(file_str)
        self._all_tests()

    def _set_up(self, text):
        self.deck_size = 10007

        self.shuffle_instrs = []
        for line in text.splitlines(keepends=False):
            self.shuffle_instrs.append(ShuffleInstruction(line))

        self.deck_perm = DeckPermutation.get_from_shuffle_instrs(           # type: DeckPermutation
            deck_size=self.deck_size,
            shuffle_instrs=self.shuffle_instrs
        )

    def _all_tests(self):
        self._deck_perm_test()
        self._perm_power_simpletest()
        self._perm_power_test()

    def _deck_perm_test(self):
        deck_perm_action = self.deck_perm.execute(list(range(self.deck_size)))

        shuffle_instrs_action = list(range(self.deck_size))
        for instr in self.shuffle_instrs:
            shuffle_instrs_action = instr.execute(shuffle_instrs_action)

        self.assertEqual(shuffle_instrs_action, deck_perm_action)

    def _perm_power_simpletest(self):
        p = 2
        perm_power = self.deck_perm.power(p)
        simple_power = self.deck_perm
        for _ in range(p):
            simple_power = self.deck_perm.multiply_by_perm(self.deck_perm)

        self.assertEqual(
            perm_power,
            simple_power,
            msg='Deck perm {}; .power({})={}; iterative={}'.format(self.deck_perm, p, perm_power, simple_power)
        )

    def _perm_power_test(self):
        p = 2
        perm_power = self.deck_perm.power(p)
        perm_power_action = perm_power.execute(list(range(self.deck_size)))
        deck_perm_action = list(range(self.deck_size))
        for _ in range(p):
            deck_perm_action = self.deck_perm.execute(deck_perm_action)

        self.assertEqual(perm_power_action, deck_perm_action, msg='.power({})={}'.format(p, perm_power))


if __name__ == "__main__":
    # unittest.main()

    with open('input/dec22.txt', 'r') as file:
        the_shuffle_instrs = parse_input(file.read())
    print('Part 1:', part_1(the_shuffle_instrs))
    print('Part 2:', part_2(the_shuffle_instrs))
