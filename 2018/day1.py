from getinput import get_input
import itertools
import textwrap


def parse_input(s):
    return list(int(line) for line in s.splitlines(keepends=False))


def part_1(input_str):
    changes = parse_input(input_str)
    return sum(changes)


def part_2(input_str):
    changes = parse_input(input_str)
    freqs = set()
    freq = 0
    cursor = 0
    while freq not in freqs:
        freqs.add(freq)
        freq += changes[cursor]
        cursor = (cursor + 1) % len(changes)
    return freq


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(1)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
