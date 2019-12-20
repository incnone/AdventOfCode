from getinput import get_input
from util import grouper
import itertools
import textwrap


def parse_input(big_str):
    containers = []
    for line in big_str.splitlines(keepends=False):
        containers.append(int(line))
    return containers


def part_1(containers):
    desired_amt = 150
    num_ways = 0
    for num in range(len(containers)+1):
        for perm in itertools.combinations(containers, num):
            if sum(perm) == desired_amt:
                num_ways += 1
    return num_ways


def part_2(containers):
    desired_amt = 150
    num_ways = 0
    for num in range(len(containers)+1):
        for perm in itertools.combinations(containers, num):
            if sum(perm) == desired_amt:
                num_ways += 1
        if num_ways > 0:
            break
    return num_ways


if __name__ == "__main__":
    the_containers = parse_input(get_input(day=17))

    print('Part 1:', part_1(the_containers))
    print('Part 2:', part_2(the_containers))
