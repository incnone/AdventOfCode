from getinput import get_input
import itertools
import textwrap
from collections import Counter


def parse_input(s):
    claims = []
    for line in s.splitlines(keepends=False):
        words = line.split()
        ul = tuple(int(x) for x in words[2].rstrip(':').split(','))
        wh = tuple(int(x) for x in words[3].split('x'))
        claims.append((*ul, *wh))
    return claims


def get_all_claimed(claim):
    return set(itertools.product(range(claim[0], claim[0]+claim[2]), range(claim[1], claim[1]+claim[3])))


def part_1(input_str):
    claims = parse_input(input_str)
    c = Counter()
    for claim in claims:
        c.update(get_all_claimed(claim))
    return sum(1 for x in c.values() if x > 1)


def part_2(input_str):
    claims = parse_input(input_str)
    c = Counter()
    for claim in claims:
        c.update(get_all_claimed(claim))

    for idx, claim in enumerate(claims):
        if not any(c[sq] > 1 for sq in get_all_claimed(claim)):
            return idx+1


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(3)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
