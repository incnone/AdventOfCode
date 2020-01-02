from getinput import get_input
import itertools
import textwrap
from twosidedtape import TwoSidedTape


class PlantLine(object):
    def __init__(self, initial_state, rules):
        self.state = TwoSidedTape()
        for idx, val in enumerate(initial_state):
            self.state[idx] = val
        self.rules = rules
        self.cursor = 0

    def __str__(self):
        left, right = self.state.bounds()
        return ''.join('#' if self.state[idx] else ' ' for idx in range(left, right))

    def grows_plant(self, idx):
        a, b, c, d, e = self.state[idx-2], self.state[idx-1], self.state[idx], self.state[idx+1], self.state[idx+2]
        if (a, b, c, d, e) in self.rules:
            return self.rules[(a, b, c, d, e)]
        else:
            return False

    def evolve(self):
        left, right = self.state.bounds()
        new_state = TwoSidedTape()
        for idx in range(left-2, right+2):
            new_state[idx] = self.grows_plant(idx)
        self.state = new_state


def parse_input(s: str):
    lines = s.splitlines(keepends=False)
    initial_state = tuple(True if c == '#' else False for c in lines[0][15:])
    rules = dict()
    for line in lines[2:]:
        words = line.split(' => ')
        rules[tuple(True if c == '#' else False for c in words[0])] = True if words[1] == '#' else False
    return initial_state, rules


def part_1(input_str: str):
    # input_str = test_input()
    plants = PlantLine(*parse_input(input_str))
    for x in range(20):
        plants.evolve()
    return sum(idx for idx in range(*plants.state.bounds()) if plants.state[idx])


def part_2(input_str: str):
    plants = PlantLine(*parse_input(input_str))

    # Plant pattern stabilizes at 182 cycles or so, then shifts right one square forever
    stable_cycle = 200
    for x in range(stable_cycle):
        plants.evolve()

    shift = (50000000000 - stable_cycle)
    return sum(idx+shift for idx in range(*plants.state.bounds()) if plants.state[idx])


def test_input():
    return textwrap.dedent("""\
    initial state: #..#.#..##......###...###

    ...## => #
    ..#.. => #
    .#... => #
    .#.#. => #
    .#.## => #
    .##.. => #
    .#### => #
    #.#.# => #
    #.### => #
    ##.#. => #
    ##.## => #
    ###.. => #
    ###.# => #
    ####. => #""")


def main():
    input_str = get_input(12)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
