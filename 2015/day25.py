from getinput import get_input
from util import ncr


def get_idx(row, col):
    if row == col == 1:
        return 1
    return ncr(row+col-1, 2) + col


def get_val(row, col):
    mod = 33554393
    rat = 252533
    startval = 20151125
    return startval*pow(rat, get_idx(row, col)-1, mod) % mod


def parse_input(s):
    words = s.split()
    return int(words[-1].rstrip('.')), int(words[-3].rstrip(','))


def part_1(row, col):
    return get_val(row, col)


if __name__ == "__main__":
    the_col, the_row = parse_input(get_input(25))
    print(the_row, the_col)
    print('Part 1:', part_1(the_row, the_col))
