from getinput import get_input
import itertools
import textwrap
import string
import re


def parse_input(s):
    return s


def reacting_pair(c, d):
    return abs(ord(c) - ord(d)) == ord('a') - ord('A')


def react(s):
    skip = False
    t = ''
    for c, d in zip(s, s[1:]):
        if skip:
            skip = False
            continue
        if reacting_pair(c, d):
            skip = True
            continue
        t += c

    if not skip:
        t += s[-1]

    return t


def fully_react(s):
    # This is stupid slow, and I could do better, say by finding all immediate reactions and then "propagating them
    # outwards", so as to fully reduce the string in one iteration
    last_string = s
    s = react(s)
    while len(s) != len(last_string):
        last_string = s
        s = react(s)
    return s


def part_1(input_str):
    # input_str = test_input()
    return len(fully_react(input_str))


def part_2(input_str):
    # input_str = test_input()
    lengths = dict()
    for c in string.ascii_lowercase:
        d = c.upper()
        lengths[c] = len(fully_react(re.sub(r'[{}{}]'.format(c, d), '', input_str)))

    return min(lengths.values())


def test_input():
    return textwrap.dedent("""\
    dabAcCaCBAcCcaDA""")


def main():
    input_str = get_input(5)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
