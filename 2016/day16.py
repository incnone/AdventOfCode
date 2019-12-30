from getinput import get_input
from util import grouper


def dragonize(s):
    return s + '0' + ''.join('1' if x == '0' else '0' for x in reversed(s))


def checksum(s):
    cs = ''.join('1' if a == b else '0' for a, b in grouper(s, 2))
    if len(cs) % 2 == 0:
        return checksum(cs)
    else:
        return cs


def part_1(big_str):
    length = 272
    while len(big_str) < length:
        big_str = dragonize(big_str)
    return checksum(big_str[:length])


def part_2(big_str):
    length = 35651584
    while len(big_str) < length:
        big_str = dragonize(big_str)
    return checksum(big_str[:length])


if __name__ == "__main__":
    the_big_str = get_input(16)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
