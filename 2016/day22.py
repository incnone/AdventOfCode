from getinput import get_input
from enum import Enum


class Node(object):
    def __init__(self, size, used):
        self.size = size
        self.used = used

    def __str__(self):
        return '{}/{}'.format(self.used, self.size)

    def __repr__(self):
        return '{}/{}'.format(self.used, self.size)

    @property
    def avail(self):
        return self.size - self.used


class SimpleNode(Enum):
    OPEN = 0
    BLOCK = 1
    WALL = 2
    DATA = 3

    @property
    def chr(self):
        chrdict = {
            SimpleNode.OPEN: '_',
            SimpleNode.BLOCK: '.',
            SimpleNode.WALL: '#',
            SimpleNode.DATA: 'G',
        }
        return chrdict[self]


def parse_input(s):
    node_dict = dict()
    for line in s.splitlines(keepends=False):
        words = line.split()
        loc = tuple(int(k[1:]) for k in words[0].split('-')[1:])
        size, used, avail = tuple(int(k[:-1]) for k in words[1:-1])
        assert avail == size - used
        node_dict[loc] = Node(size=size, used=used)
    return node_dict


def part_1(big_str):
    nodes = parse_input(big_str)
    viable_pairs = 0
    for locA, nodeA in nodes.items():
        if nodeA.used == 0:
            continue
        for locB, nodeB in nodes.items():
            if locA == locB:
                continue
            if nodeB.avail >= nodeA.used:
                viable_pairs += 1
    return viable_pairs


def make_simple_nodes(big_str):
    nodes = parse_input(big_str)
    xmax = max(x for x, y in nodes.keys() if y == 0)
    simple_nodes = dict()
    for loc, node in nodes.items():
        if loc == (xmax, 0):
            simple_nodes[loc] = SimpleNode.DATA
        elif node.used > 400:
            simple_nodes[loc] = SimpleNode.WALL
        elif node.used == 0:
            simple_nodes[loc] = SimpleNode.OPEN
        else:
            simple_nodes[loc] = SimpleNode.BLOCK
    return simple_nodes


def simple_nodes_str(nodes):
    xmax = max(k[0] for k in nodes.keys()) + 1
    ymax = max(k[1] for k in nodes.keys()) + 1
    return '\n'.join(''.join(nodes[(x, y)].chr for x in range(xmax)) for y in range(ymax))


def part_2(big_str):
    nodes = make_simple_nodes(big_str)
    # Use this picture to solve by hand
    return simple_nodes_str(nodes)


if __name__ == "__main__":
    the_big_str = get_input(22)

    # print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
