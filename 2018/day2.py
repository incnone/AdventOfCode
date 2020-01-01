from getinput import get_input
import itertools
import textwrap
from collections import Counter


def parse_input(s):
    return list(s.splitlines(keepends=False))


def part_1(input_str):
    num_2 = 0
    num_3 = 0
    for s in parse_input(input_str):
        c = Counter(s)
        num_2 += 1 if 2 in c.values() else 0
        num_3 += 1 if 3 in c.values() else 0
    return num_2*num_3


def num_different(s1, s2):
    return sum(1 if c != d else 0 for c, d in zip(s1, s2))


def part_2(input_str):
    presents = parse_input(input_str)
    for s1, s2 in itertools.combinations(presents, 2):
        if num_different(s1, s2) == 1:
            return ''.join(c for c, d in zip(s1, s2) if c == d)


def test_input():
    return textwrap.dedent("""\
    abcdef
    bababc
    abbcde
    abcccd
    aabcdd
    abcdee
    ababab""")


def main():
    input_str = get_input(2)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
