import textwrap
import string
from typing import List
from collections import defaultdict


class BagContent(object):
    def __init__(self, wds: List[str]):
        self.num = int(wds[0])
        self.shade = wds[1]
        self.color = wds[2]

    def __str__(self):
        return '{n} {s} {c} bags'.format(n=self.num, s=self.shade, c=self.color)

    @property
    def fullcolor(self):
        return '{} {}'.format(self.shade, self.color)


class BagRule(object):
    def __init__(self, s: str):
        s = s.rstrip('\n')
        words = s.split()
        self.shade = words[0]
        self.color = words[1]
        self.contents = []
        if not s.endswith('no other bags.'):
            num_contents = len(words[4:])//4
            for idx in range(num_contents):
                self.contents.append(BagContent(words[4+4*idx:8+4*idx]))

    def __str__(self):
        cts_str = ','.join(str(c) for c in self.contents)
        return '{s} {c} bags contain {cts}'.format(s=self.shade, c=self.color, cts=cts_str)

    @property
    def fullcolor(self):
        return '{} {}'.format(self.shade, self.color)


def get_test_input() -> str:
    # return textwrap.dedent("""\
    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    # dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    # bright white bags contain 1 shiny gold bag.
    # muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    # dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    # faded blue bags contain no other bags.
    # dotted black bags contain no other bags.""")
    return textwrap.dedent("""\
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(BagRule(line))
    return data


def part_1(data):
    contained_by_graph = defaultdict(lambda: [])
    for bag_rule in data:
        for content in bag_rule.contents:
            contained_by_graph[content.fullcolor].append(bag_rule.fullcolor)

    # DFS on contained by graph
    init_node = 'shiny gold'
    nodes = [init_node]
    searched = {init_node}
    while nodes:
        front = nodes.pop(0)
        for x in contained_by_graph[front]:
            if x not in searched:
                searched.add(x)
                nodes.append(x)

    print('Part 1:', len(searched) - 1)


def part_2(data):
    bag_rules_dict = dict()
    for bag_rule in data:
        bag_rules_dict[bag_rule.fullcolor] = bag_rule.contents

    # DFS on containing graph
    init_node = 'shiny gold'
    nodes = [(init_node, 1)]
    num_bags = 0
    while nodes:
        front = nodes.pop(0)
        num_bags += front[1]
        for bag_content in bag_rules_dict[front[0]]:
            nodes.append((bag_content.fullcolor, bag_content.num*front[1]))

    print('Part 2:', num_bags - 1)


def main():
    data = read_input(day_number=7, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
