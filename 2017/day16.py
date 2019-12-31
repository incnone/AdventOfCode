from getinput import get_input
import string
import itertools


class Dance(object):
    @staticmethod
    def permutation_power(perm, power):
        new_perm = dict()
        for x in perm.keys():
            # Find order of x in the permutation
            order = 1
            v = perm[x]
            while v != x:
                v = perm[v]
                order += 1

            # Use division
            pwr_remainder = power % order
            v = x
            for _ in range(pwr_remainder):
                v = perm[v]
            new_perm[x] = v
        return new_perm

    @staticmethod
    def power(dance, power):
        new_dance = Dance(dance.num_players, [])
        new_dance.permutation = Dance.permutation_power(dance.permutation, power)
        new_dance.relabelling = Dance.permutation_power(dance.relabelling, power)
        return new_dance

    def __init__(self, players, moves):
        self.permutation = dict()
        self.relabelling = dict()
        self.num_players = players
        for x in range(players):
            self.permutation[x] = x
            self.relabelling[x] = x
        for move in moves:
            self.add_move(move)

    def do_dance(self):
        vals = list(self.relabelling[self.permutation[idx]] for idx in range(self.num_players))
        return ''.join(chr(ord('a') + x) for x in vals)

    def add_move(self, move):
        # Spin
        if move[0] == 's':
            new_perm = dict()
            spin = int(move[1:])
            for x in self.permutation.keys():
                new_perm[x] = self.permutation[(x - spin) % self.num_players]
            self.permutation = new_perm

        # Exchange
        elif move[0] == 'x':
            a, b = tuple(int(x) for x in move[1:].split('/'))
            self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]

        # Partner
        elif move[0] == 'p':
            a, b = tuple((ord(x) - ord('a')) for x in move[1:].split('/'))
            for x, y in self.relabelling.items():
                if y == a:
                    self.relabelling[x] = b
                elif y == b:
                    self.relabelling[x] = a


def parse_input(s):
    return s.split(',')


def execute_move(dance_move, s):
    # Spin
    if dance_move[0] == 's':
        spin = int(dance_move[1:])
        return s[-spin:] + s[:-spin]

    # Exchange
    elif dance_move[0] == 'x':
        pos = list(int(x) for x in dance_move[1:].split('/'))
        a = min(pos)
        b = max(pos)
        return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

    # Partner
    elif dance_move[0] == 'p':
        pos = list(s.index(x) for x in dance_move[1:].split('/'))
        a = min(pos)
        b = max(pos)
        return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]


def part_1(input_str):
    return Dance(16, parse_input(input_str)).do_dance()


def part_2(input_str):
    return Dance.power(Dance(16, parse_input(input_str)), 10**9).do_dance()


def test_input():
    return "s1,x3/4,pe/b"


def main():
    input_str = get_input(16)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
