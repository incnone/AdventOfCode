from getinput import get_input
from collections import Counter


def part_1(big_str):
    msg = ''
    for idx in range(8):
        c = Counter(s[idx] for s in big_str.splitlines(keepends=False))
        msg += max(c.keys(), key=lambda x: c[x])
    return msg


def part_2(big_str):
    msg = ''
    for idx in range(8):
        c = Counter(s[idx] for s in big_str.splitlines(keepends=False))
        msg += min(c.keys(), key=lambda x: c[x])
    return msg


if __name__ == "__main__":
    the_big_str = get_input(6)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
