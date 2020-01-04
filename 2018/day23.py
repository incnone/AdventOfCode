from getinput import get_input
import itertools
import textwrap
import re
from grid import Loc2


class Octahedron(object):
    idx = 0

    @staticmethod
    def intersection(oct_1, oct_2):
        o = Octahedron()
        for idx in range(4):
            vmin = max(oct_1.vals[idx][0], oct_2.vals[idx][0])
            vmax = min(oct_1.vals[idx][1], oct_2.vals[idx][1])
            if vmax < vmin:
                return None
            o.vals.append((vmin, vmax))
        return o

    @staticmethod
    def from_center_and_r(center, radius):
        o = Octahedron()
        center_offsets = [
            center[0] + center[1] + center[2],
            center[0] + center[1] - center[2],
            center[0] - center[1] + center[2],
            center[0] - center[1] - center[2]
        ]
        o.vals = [(-radius + c, radius + c) for c in center_offsets]
        return o

    def __init__(self):
        """
        A grid-aligned octahedron is the intersection of 8 half-spaces:
             a1 <= x + y + z <= a2
             b1 <= x + y - z <= b2
             c1 <= x - y + z <= c2
             d1 <= x - y - z <= d2
        We represent this by the list [(a1, a2), (b1, b2), (c1, c2), (d1, d2)].
        """
        self.vals = []
        self.idx = Octahedron.idx
        Octahedron.idx += 1

    def __hash__(self):
        return hash(tuple(self.vals))

    def __str__(self):
        return 'O{}'.format(str(self.vals))

    def __repr__(self):
        return 'T{}'.format(self.idx)


def parse_input(s: str):
    particles = []
    for line in s.splitlines(keepends=False):
        pos = tuple(int(x) for x in (re.findall(r'pos=<(-?\d*),(-?\d*),(-?\d*)>', line))[0])
        r = int(re.findall(r'r=(\d*)', line)[0])
        particles.append((pos, r))
    return particles


def part_1(input_str: str):
    # input_str = test_input(1)
    nanobots = parse_input(input_str)
    center, dist = max(nanobots, key=lambda p: p[1])
    num_in_range = 0
    for loc, r in nanobots:
        if sum(abs(loc[x] - center[x]) for x in range(3)) <= dist:
            num_in_range += 1
    return num_in_range


def part_2(input_str: str):
    # input_str = test_input(2)
    nanobots = parse_input(input_str)
    initial_octs = []
    for loc, r in nanobots:
        initial_octs.append(Octahedron.from_center_and_r(loc, r))

    intersection_count = 1
    intersections = dict()
    for o in initial_octs:
        intersections[frozenset({o})] = o

    while True:
        new_intersections = dict()
        for oct_set, intersection in intersections.items():
            for oct in initial_octs:
                if oct not in oct_set:
                    new_intersection = Octahedron.intersection(intersection, oct)
                    if new_intersection is not None:
                        new_intersections[frozenset(oct_set.union({oct}))] = new_intersection
        if not new_intersections:
            break
        intersections = new_intersections
        intersection_count += 1
        print(intersection_count)

    print(intersection_count)
    print(intersections)
    for t in intersections.values():
        print(t)


def test_input(test_num):
    if test_num == 1:
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
    elif test_num == 2:
        return textwrap.dedent("""\
        pos=<10,12,12>, r=2
        pos=<12,14,12>, r=2
        pos=<16,12,12>, r=4
        pos=<14,14,14>, r=6
        pos=<50,50,50>, r=200
        pos=<10,10,10>, r=5""")


def main():
    input_str = get_input(23)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
