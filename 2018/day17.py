from getinput import get_input
import itertools
import textwrap
import re
from grid import Loc2, Direction


class Reservoir(object):
    def __init__(self, clay_tiles):
        self.clay = clay_tiles
        self.water = set()
        self.spigot = Loc2(500, 0)
        self.active_wet = {self.spigot}
        self.wet = {self.spigot}
        self.x_bounds = (min(loc.x for loc in self.clay), max(loc.x for loc in self.clay))
        self.y_bounds = (min(min(loc.y for loc in self.clay), 0), max(loc.y for loc in self.clay))

    @property
    def num_water(self):
        ymin, ymax = self.y_bounds
        return sum(1 for p in self.wet if ymin <= p.y <= ymax) + sum(1 for p in self.water if ymin <= p.y <= ymax)

    def clay_or_water_at(self, loc):
        return loc in self.clay or loc in self.water

    def wet_at(self, loc):
        return loc in self.wet

    def sand_at(self, loc):
        return loc not in self.clay and loc not in self.water and loc not in self.wet

    def _get_char(self, x, y):
        if Loc2(x, y) == self.spigot:
            return '+'
        else:
            return '#' if Loc2(x, y) in self.clay \
                else '~' if Loc2(x, y) in self.water \
                else '|' if Loc2(x, y) in self.wet \
                else ' '

    def __str__(self):
        return '\n'.join(
            ''.join(self._get_char(x, y) for x in range(self.x_bounds[0]-2, self.x_bounds[1]+3))
            for y in range(self.y_bounds[0]-1, self.y_bounds[1]+2)
        )

    def make_water(self, steps=False, debug=False):
        if debug:
            while self.make_water_step():
                print(self)
                input()

        if steps:
            steps = 0
            while self.make_water_step():
                if steps % 100 == 0:
                    print(steps)
                steps += 1

        while self.make_water_step():
            pass

    def make_water_step(self):
        became_inactive_wet = []
        became_active_wet = []
        hit_wall = []
        for loc in self.active_wet:
            under = loc + Loc2(0, 1)

            # Below us is the void, so we're boring
            if under.y > self.y_bounds[1]:
                became_inactive_wet.append(loc)

            # Below us is clay or standing water, so spread sideways and never check this tile again
            elif self.clay_or_water_at(under):
                became_inactive_wet.append(loc)
                for d in [Direction.WEST, Direction.EAST]:
                    side = loc + d
                    if side in self.clay or side in self.wet:
                        hit_wall.append(loc)
                    else:
                        became_active_wet.append(side)

            # Below us is sand, so make it wet
            elif under not in self.wet:
                became_active_wet.append(under)

        activity = became_active_wet or hit_wall

        # Manage wetness activity
        for loc in became_inactive_wet:
            self.active_wet.remove(loc)
        for loc in became_active_wet:
            self.active_wet.add(loc)
            self.wet.add(loc)

        # Manage walls
        new_standing_water = []
        for loc in hit_wall:
            sides = [None, None]
            for idx, d in enumerate([Direction.WEST, Direction.EAST]):
                side_loc = loc
                while side_loc in self.wet:
                    side_loc = side_loc + d
                sides[idx] = side_loc
            left, right = sides
            if left in self.clay and right in self.clay:
                next_loc = left + Direction.EAST
                while next_loc != right:
                    new_standing_water.append(next_loc)
                    next_loc = next_loc + Direction.EAST
        for loc in new_standing_water:
            self.active_wet.discard(loc)
            self.wet.discard(loc)
            self.water.add(loc)

        return activity


def parse_input(s: str):
    clay_tiles = set()
    for line in s.splitlines(keepends=False):
        vert = re.findall(r'x=(\d*), y=(\d*)..(\d*)', line)
        if vert:
            x, ymin, ymax = (int(t) for t in vert[0])
            for y in range(ymin, ymax+1):
                clay_tiles.add(Loc2(x, y))
        horiz = re.findall(r'y=(\d*), x=(\d*)..(\d*)', line)
        if horiz:
            y, xmin, xmax = (int(t) for t in horiz[0])
            for x in range(xmin, xmax+1):
                clay_tiles.add(Loc2(x, y))
    return clay_tiles


def part_1(input_str: str):
    # # input_str = test_input()
    # reservoir = Reservoir(parse_input(input_str))
    # reservoir.make_water(steps=True)
    # with open('reservoir/end.txt', 'w') as file:
    #     file.write(str(reservoir))
    #
    # for t in reservoir.wet:
    #     assert t not in reservoir.clay and t not in reservoir.water
    #     assert t.y <= reservoir.y_bounds[1]
    #     if t.y <= 0:
    #         print(t)
    # for t in reservoir.water:
    #     assert t not in reservoir.clay
    #     assert t.y <= reservoir.y_bounds[1]
    #     if t.y <= 0:
    #         print(t)
    #
    # return len(reservoir.wet.union(reservoir.water)) - 1

    num = 0
    with open('reservoir/end.txt', 'r') as file:
        for line in file:
            for c in line:
                if c in ['~', '|']:
                    num += 1
    return num


def part_2(input_str: str):
    num = 0
    with open('reservoir/end.txt', 'r') as file:
        for line in file:
            for c in line:
                if c in ['~']:
                    num += 1
    return num


def test_input():
    return textwrap.dedent("""\
    x=495, y=2..7
    y=7, x=495..501
    x=501, y=3..7
    x=498, y=2..4
    x=506, y=1..2
    x=498, y=10..13
    x=504, y=10..13
    y=13, x=498..504
    y=10, x=505..507""")


def main():
    input_str = get_input(17)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
