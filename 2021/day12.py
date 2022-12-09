import textwrap
from collections import defaultdict
from typing import Tuple


def get_test_input() -> str:
    return textwrap.dedent("""\
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line.split('-'))
    return data


class Cave(object):
    def __init__(self, name):
        self.name = name
        self.links = set()
        self.small = name.islower()
        self.special = name in ['start', 'end']

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def get_cave_system(data):
    cave_dict = dict()
    for c1, c2 in data:
        if c1 not in cave_dict:
            cave_dict[c1] = Cave(c1)
        if c2 not in cave_dict:
            cave_dict[c2] = Cave(c2)
        cave1 = cave_dict[c1]
        cave2 = cave_dict[c2]
        cave1.links.add(cave2)
        cave2.links.add(cave1)

    return cave_dict.values(), cave_dict['start'], cave_dict['end']


def part_1(data):
    caves, start, end = get_cave_system(data)
    paths_to_check = [(start,)]
    paths = []
    while paths_to_check:
        path = paths_to_check.pop()
        for cave in path[-1].links:
            if cave == end:
                paths.append(path + (end,))
            elif cave not in path or not cave.small:
                paths_to_check.append(path + (cave,))

    print(f'Part 1: {len(paths)}')


class CavePath(object):
    def __init__(self, p):
        self.path = p
        self.double = False

    def tail(self) -> Cave:
        return self.path[-1]

    def can_append(self, c: Cave):
        return not (c.small and c in self.path) or (not self.double and not c.special)

    def get_with_append(self, c: Cave):
        ret = CavePath(self.path + (c,))
        ret.double = self.double or (c.small and c in self.path)
        return ret


def part_2(data):
    caves, start, end = get_cave_system(data)
    paths_to_check = [CavePath((start,))]
    paths = []
    while paths_to_check:
        path = paths_to_check.pop()
        for cave in path.tail().links:
            if cave == end:
                paths.append(path.get_with_append(end))
            elif path.can_append(cave):
                paths_to_check.append(path.get_with_append(cave))

    print(f'Part 2: {len(paths)}')


def main():
    data = read_input(day_number=12, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
