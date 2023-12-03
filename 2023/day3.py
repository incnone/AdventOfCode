import textwrap
from typing import List
import itertools


def get_test_input() -> str:
    return textwrap.dedent("""\
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def adj_pairs(p):
    return [
        (p[0] - 1, p[1] - 1),
        (p[0]    , p[1] - 1),
        (p[0] + 1, p[1] - 1),

        (p[0] - 1, p[1]),
        (p[0] + 1, p[1]),

        (p[0] - 1, p[1] + 1),
        (p[0]    , p[1] + 1),
        (p[0] + 1, p[1] + 1),
    ]


class Schematic(object):
    def __init__(self, s: List[str]):
        self.srep = s
        self.w = len(s[0])
        self.h = len(s)
        self.numbers = dict()
        self.part_numbers = dict()
        self.part_numbers_transp = dict()
        self.symbols = dict()
        self.part_number_locs = set()
        self.gear_numbers = dict()
        self._identify_numbers()
        self._identify_part_numbers()
        self._identify_gear_numbers()

    def __str__(self):
        return '\n'.join(self.srep)

    def get_reduced(self):
        s = ''
        for line in range(self.h):
            for c in range(self.w):
                loc = (c, line)
                if loc in self.part_number_locs:
                    s += self.srep[line][c]
                elif loc in self.symbols:
                    s += '*'
                elif self.srep[line][c] != '.':
                    s += 'x'
                else:
                    s += ' '
            s += '\n'
        return s

    def _identify_numbers(self):
        digits = '0123456789'
        self.numbers.clear()
        self.symbols.clear()
        for line_idx, line in enumerate(self.srep):
            curr_num = ''
            for val_idx, val in enumerate(line + '.'):
                val_in_digits = val in digits
                if val_in_digits:
                    curr_num += val
                elif curr_num != '':
                    loc = val_idx - len(curr_num)
                    self.numbers[(loc, line_idx)] = curr_num
                    curr_num = ''

                if val != '.' and not val_in_digits:
                    self.symbols[(val_idx, line_idx)] = val

    def _identify_part_numbers(self):
        for loc, symb in self.symbols.items():
            aps = adj_pairs(loc)
            for numloc, num in self.numbers.items():
                numlocs = [(numloc[0] + i, numloc[1]) for i in range(len(num))]
                for nloc in numlocs:
                    if nloc in aps:
                        self.part_numbers[numloc] = num
                        self.part_numbers_transp[(numloc[1], numloc[0])] = num
                        for n in numlocs:
                            self.part_number_locs.add(n)

    def _identify_gear_numbers(self):
        for loc, symb in self.symbols.items():
            if symb != '*':
                continue
            aps = adj_pairs(loc)
            adj_gears = dict()
            for numloc, num in self.numbers.items():
                numlocs = [(numloc[0] + i, numloc[1]) for i in range(len(num))]
                for nloc in numlocs:
                    if nloc in aps:
                        adj_gears[numloc] = num
            if len(adj_gears) == 2:
                vals = [int(x) for x in adj_gears.values()]
                self.gear_numbers[loc] = vals[0] * vals[1]

    def sum_parts(self):
        for x, y in itertools.product(range(self.w), range(self.h)):
            pass


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return Schematic(data)


def part_1(data):
    print(f'Part 1: {sum(int(x) for x in data.part_numbers.values())}')


def part_2(data):
    print(f'Part 2: {sum(x for x in data.gear_numbers.values())}')


def main():
    data = read_input(day_number=3, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
