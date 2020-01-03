from getinput import get_input
import itertools
import textwrap
import re
from grid import Loc2


"""Oh dang these are octahedrons oops"""


class Diamond(object):
    @staticmethod
    def intersection(dmd_1, dmd_2):
        t = Diamond(0, 0, 0, 0)

        if dmd_1.top_x <= dmd_2.top_x:
            left, right = dmd_1, dmd_2
        else:
            left, right = dmd_2, dmd_1
        t_lsum = left.top_x + left.top_y
        t_rdiff = right.top_x - right.top_y
        t.top_x = (1/2)*(t_lsum + t_rdiff)
        t.top_y = (1/2)*(t_lsum - t_rdiff)

        b_ldiff = left.bot_x - left.bot_y
        b_rsum = right.bot_x + right.bot_y
        t.bot_x = (1/2)*(b_rsum + b_ldiff)
        t.bot_y = (1/2)*(b_rsum - b_ldiff)
        return t if t.valid else None

    def __init__(self, top_x, top_y, bot_x, bot_y):
        self.top_x = top_x
        self.top_y = top_y
        self.bot_x = bot_x
        self.bot_y = bot_y

    def __hash__(self):
        return hash((self.top_x, self.top_y, self.bot_x, self.bot_y))

    def __str__(self):
        return 'Dmd:({},{})->({},{})'.format(self.top_x, self.top_y, self.bot_x, self.bot_y)

    def __repr__(self):
        return str(self)

    @property
    def valid(self):
        return self.bot_y > self.top_y and (self.bot_y - self.top_y) > abs(self.bot_x - self.top_x)


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
    input_str = test_input(2)
    nanobots = parse_input(input_str)
    diamonds = []
    for loc, r in nanobots:
        diamonds.append(Diamond(top_x=loc[0], top_y=loc[1]-r, bot_x=loc[0], bot_y=loc[1]+r))

    intersection_count = 1
    intersections = [(d, {d}) for d in diamonds]
    while True:
        new_intersections = []
        for dmd, incl_diamonds in intersections:
            for d in diamonds:
                if d not in incl_diamonds:
                    new_inter = Diamond.intersection(d, dmd)
                    if new_inter is not None:
                        new_intersections.append((new_inter, incl_diamonds.union({d})))
        if not new_intersections:
            break
        intersections = new_intersections
        intersection_count += 1
    print(intersection_count)
    print(intersections)


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
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
