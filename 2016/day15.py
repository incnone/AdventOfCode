from getinput import get_input
from util import solve_crt


class Disc(object):
    def __init__(self, num_positions, initial_position):
        self.num_positions = num_positions
        self.position = initial_position

    def __str__(self):
        return '{}/{}'.format(self.position, self.num_positions)

    def __repr__(self):
        return str(self)


def parse_input(s):
    discs = dict()
    for line in s.splitlines(keepends=False):
        words = line.split()
        discs[int(words[1].lstrip('#'))] = Disc(int(words[3]), int(words[-1].rstrip('.')))
    return discs


def part_1(big_str):
    discs = parse_input(big_str)
    congs = tuple()
    mods = tuple()
    for num, disc in discs.items():
        congs += ((disc.num_positions - disc.position - num) % disc.num_positions,)
        mods += (disc.num_positions,)
    return solve_crt(congs, mods)


def part_2(big_str):
    discs = parse_input(big_str)
    discs[7] = Disc(num_positions=11, initial_position=0)
    congs = tuple()
    mods = tuple()
    for num, disc in discs.items():
        congs += ((disc.num_positions - disc.position - num) % disc.num_positions,)
        mods += (disc.num_positions,)
    return solve_crt(congs, mods)


if __name__ == "__main__":
    the_big_str = get_input(15)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
