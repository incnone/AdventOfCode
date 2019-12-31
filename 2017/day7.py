from getinput import get_input
import itertools
import textwrap
from collections import defaultdict


class Program(object):
    def __init__(self, name, weight, children):
        self.name = name
        self.disc_weight = weight
        self.children = children

    def __str__(self):
        return '({}) -> {}'.format(self.weight, self.children)

    def __repr__(self):
        return str(self)

    @property
    def weight(self):
        return self.disc_weight + sum(child.weight for child in self.children)


def parse_input(s):
    programs = dict()
    for line in s.splitlines(keepends=False):
        words = line.split()
        children = []
        if len(words) > 2:
            children = [x.rstrip(',') for x in words[3:]]
        programs[words[0]] = Program(name=words[0], weight=int(words[1].strip('()')), children=children)

    for prog in programs.values():
        prog.children = list([programs[name] for name in prog.children])

    return programs


def get_base(programs):
    children = set()
    for prog in programs.values():
        for child in prog.children:
            children.add(child.name)
    for name in programs.keys():
        if name not in children:
            return programs[name]


def part_1(input_str):
    # input_str = test_input()
    programs = parse_input(input_str)
    return get_base(programs).name


def find_odd_weight(tower, desired_weight):
    weights = defaultdict(lambda: [])
    for child in tower.children:
        weights[child.weight].append(child)

    # If this tower is balanced, then it's this weight we need to change
    if len(weights) == 1:
        return tower.disc_weight + (desired_weight - tower.weight)

    # Otherwise, go one level deeper to the odd tower
    common_weight = None
    for weight, subtowers in weights.items():
        if len(subtowers) > 1:
            common_weight = weight
    for weight, subtowers in weights.items():
        if len(subtowers) == 1:
            return find_odd_weight(subtowers[0], common_weight)


def part_2(input_str):
    # input_str = test_input()
    programs = parse_input(input_str)
    return find_odd_weight(get_base(programs), 0)


def test_input():
    return textwrap.dedent("""\
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)""")


def main():
    input_str = get_input(7)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
