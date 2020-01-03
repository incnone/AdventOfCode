from getinput import get_input
import itertools
import textwrap
import re


def parse_input(s: str):
    particles = []
    for line in s.splitlines(keepends=False):
        pos = tuple(int(x) for x in (re.findall(r'pos=<(-?\d*),(-?\d*),(-?\d*)>', line))[0])
        r = int(re.findall(r'r=(\d*)', line)[0])
        particles.append((pos, r))
    return particles


def part_1(input_str: str):
    # input_str = test_input()
    nanobots = parse_input(input_str)
    center, dist = max(nanobots, key=lambda p: p[1])
    num_in_range = 0
    for loc, r in nanobots:
        if sum(abs(loc[x] - center[x]) for x in range(3)) <= dist:
            num_in_range += 1
    return num_in_range


def part_2(input_str: str):
    return


def test_input():
    return textwrap.dedent("""\
    pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1""")


def main():
    input_str = get_input(23)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
