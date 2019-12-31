from getinput import get_input
import itertools


def sign(n):
    return -1 if n < 0 else (1 if n > 0 else 0)


class HexLoc(object):
    @staticmethod
    def dist(loc_1, loc_2):
        n_disp = loc_1.n - loc_2.n
        se_disp = loc_1.se - loc_2.se
        if sign(n_disp) == sign(se_disp):
            return abs(n_disp) + abs(se_disp) - min(abs(n_disp), abs(se_disp))
        else:
            return abs(n_disp) + abs(se_disp)

    @staticmethod
    def add_dir(hexloc, d: str):
        if d == 'n':
            return HexLoc(hexloc.se, hexloc.n + 1)
        if d == 's':
            return HexLoc(hexloc.se, hexloc.n - 1)
        if d == 'se':
            return HexLoc(hexloc.se + 1, hexloc.n)
        if d == 'nw':
            return HexLoc(hexloc.se - 1, hexloc.n)
        if d == 'ne':
            return HexLoc(hexloc.se + 1, hexloc.n + 1)
        if d == 'sw':
            return HexLoc(hexloc.se - 1, hexloc.n - 1)

    def __init__(self, se, n):
        self.se = se
        self.n = n


def part_1(input_str):
    loc = HexLoc(0, 0)
    for d in input_str.split(','):
        loc = HexLoc.add_dir(loc, d)
    return HexLoc.dist(loc, HexLoc(0, 0))


def part_2(input_str):
    loc = HexLoc(0, 0)
    max_dist = 0
    for d in input_str.split(','):
        loc = HexLoc.add_dir(loc, d)
        max_dist = max(max_dist, HexLoc.dist(loc, HexLoc(0, 0)))
    return max_dist


def main():
    input_str = get_input(11)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
