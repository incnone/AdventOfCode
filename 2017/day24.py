from getinput import get_input
import itertools
from priorityqueue import PriorityQueue
from typing import FrozenSet, Tuple
import textwrap


class InvalidDominoError(RuntimeError):
    def __init__(self, *args):
        RuntimeError.__init__(self, *args)


class DominoBridge(object):
    def __init__(self, elements, end):
        self.elements = elements    # type: FrozenSet[Tuple[int, int]]
        self.end = end              # type: int

    @property
    def length(self):
        return len(self.elements)

    @property
    def strength(self):
        return sum(t[0] + t[1] for t in self.elements)

    def successor(self, domino):
        if domino in self.elements:
            raise InvalidDominoError('')

        if domino[0] == self.end:
            new_end = domino[1]
        elif domino[1] == self.end:
            new_end = domino[0]
        else:
            raise InvalidDominoError('')

        return DominoBridge(self.elements.union({domino}), new_end)

    def __hash__(self):
        return hash((self.elements, self.end))

    def __eq__(self, other):
        return self.elements == other.elements and self.end == other.end

    def __ne__(self, other):
        return not self == other


def parse_input(s):
    return list(tuple(map(int, line.split('/'))) for line in s.splitlines(keepends=False))


def both_parts(input_str):
    # input_str = test_input()
    pairs = parse_input(input_str)
    # for p, q in itertools.combinations(pairs, 2):
    #     assert p != q

    bridges = {DominoBridge(frozenset(), 0)}
    completed_bridges = set()

    while bridges:
        bridge = bridges.pop()
        found_any_succs = False
        for p in pairs:
            try:
                bridges.add(bridge.successor(p))
                found_any_succs = True
            except InvalidDominoError:
                continue
        if not found_any_succs:
            completed_bridges.add(bridge)

    max_strength = max(bridge.strength for bridge in completed_bridges)
    strength_of_max_length = max(completed_bridges, key=lambda b: (b.length, b.strength)).strength
    return max_strength, strength_of_max_length


def test_input():
    return textwrap.dedent("""\
    0/2
    2/2
    2/3
    3/4
    3/5
    0/1
    10/1
    9/10""")


def main():
    input_str = get_input(24)
    part_1, part_2 = both_parts(input_str)
    print('Part 1:', part_1)
    print('Part 2:', part_2)


if __name__ == "__main__":
    main()
