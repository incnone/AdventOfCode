import itertools
import textwrap
import math
import numpy as np


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


def get_input(day):
    with open('input/day{}.txt'.format(day), 'r') as file:
        return file.read()


def parse_input(s: str):
    particles = []
    for line in s.splitlines(keepends=False):
        pos = [int(x) for x in line.split(',')]
        particles.append((tuple(pos[:3]), pos[3]))
    return particles


def dist_taxi(p1, p2):
    return sum(abs(p1[x] - p2[x]) for x in range(len(p1)))


def part_1(nanobots: str):
    center, dist = max(nanobots, key=lambda p: p[1])
    num_in_range = 0
    for loc, _ in nanobots:
        if dist_taxi(loc, center) <= dist:
            num_in_range += 1
    return num_in_range


def part_2(nanobots):
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
            for ogon in initial_octs:
                if ogon not in oct_set:
                    new_intersection = Octahedron.intersection(intersection, ogon)
                    if new_intersection is not None:
                        new_intersections[frozenset(oct_set.union({ogon}))] = new_intersection
        if not new_intersections:
            break
        intersections = new_intersections
        intersection_count += 1
        print(intersection_count)

    print(intersection_count)
    print(intersections)
    for t in intersections.values():
        print(t)


# def get_valid_cuboids(nanobots, cuboids):
#     """cuboids are given as ((xmin, ymin, zmin), (xwidth, ywidth, zwidth))"""
#     cuboid_mins = dict()
#     cuboid_maxs = dict()
#     for loc, w in cuboids:
#         mins, maxs = 0, 0
#         center = loc + w/2
#         sum_of_w = sum(w)/2
#         for nb_pos, nb_rad in nanobots:
#             dist = dist_taxi(nb_pos, center)
#             if dist <= nb_rad - sum_of_w:    # This beacon must intersect this cuboid
#                 mins += 1
#                 maxs += 1
#             elif dist <= nb_rad + sum_of_w:  # This beacon might intersect this cuboid
#                 maxs += 1
#         cuboid_mins[tuple(loc)] = mins
#         cuboid_maxs[tuple(loc)] = maxs
#
#     max_of_mins = max(cuboid_mins.values())
#     for cuboid in cuboids:
#         if cuboid_maxs[tuple(cuboid[0])] >= max_of_mins:
#             yield cuboid
#
#
# def subdivide_cuboids(cuboids, divisions):
#     for loc, w in cuboids:
#         nw, r = divmod(w, divisions)
#         for i, j, k in itertools.product(range(divisions), range(divisions), range(divisions)):
#             yield loc + np.array([i, j, k])*nw, \
#                   nw + r * np.array([i == divisions-1, j == divisions-1, k == divisions-1])
#
#
# def part_2(nanobots):
#     init_size = 10000000
#     mins = -init_size
#     cuboids = [(np.array([mins, mins, mins]), np.array([2*init_size, 2*init_size, 2*init_size]))]
#     divisions_per_step = 3
#     num_steps = math.ceil(math.log(2*init_size, divisions_per_step))
#     print(f'Num steps: {num_steps}')
#     for i in range(num_steps):
#         subdiv_cubs = list(subdivide_cuboids(cuboids, divisions_per_step))
#         new_cuboids = get_valid_cuboids(nanobots=nanobots, cuboids=subdiv_cubs)
#         cuboids = list(new_cuboids)
#         print(i, len(cuboids))
#
#     print(cuboids)


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
    nbs = parse_input(get_input('23_clean'))
    # with open('input/day23_clean.txt', 'w') as file:
    #     for loc, r in nbs:
    #         file.write(f'{loc[0]},{loc[1]},{loc[2]},{r}\n')

    # print('Part 1:', part_1(nbs))
    part_2(nbs)


if __name__ == "__main__":
    main()
