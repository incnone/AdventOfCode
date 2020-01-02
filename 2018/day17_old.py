from getinput import get_input
import itertools
import textwrap
import re
from grid import Loc2


class Reservoir(object):
    def __init__(self, clay_tiles):
        self.clay = clay_tiles
        self.water = set()
        self.wet = set()
        self.spigot = Loc2(500, 0)
        self.active_spigots = [self.spigot]
        self.x_bounds = (min(loc.x for loc in self.clay), max(loc.x for loc in self.clay))
        self.y_bounds = (min(min(loc.y for loc in self.clay), 0), max(loc.y for loc in self.clay))

    @property
    def _claywater_iter(self):
        return itertools.chain(self.clay, self.water)

    def _get_char(self, x, y):
        if Loc2(x, y) == self.spigot:
            return '+'
        else:
            return '#' if Loc2(x, y) in self.clay \
                else '~' if Loc2(x, y) in self.water \
                else '|' if Loc2(x, y) in self.wet \
                else '.'

    def __str__(self):
        return '\n'.join(
            ''.join(self._get_char(x, y) for x in range(self.x_bounds[0], self.x_bounds[1]+1))
            for y in range(self.y_bounds[0], self.y_bounds[1]+1)
        )

    def make_water(self):
        while self.active_spigots:
            spigot = self.active_spigots.pop(0)
            self.run_spigot(spigot)

    def run_spigot(self, spigot):
        moving_spigot = spigot
        while moving_spigot not in self._claywater_iter:
            if moving_spigot.y > self.y_bounds[1]:
                return
            if moving_spigot.y > 0:
                self.wet.add(moving_spigot)
            moving_spigot = moving_spigot + Loc2(0, 1)
        moving_spigot = moving_spigot - Loc2(0, 1)
        # print(source)

        # Find left/right bounds
        new_sources = []
        left = right = moving_spigot
        while left not in self.clay:
            self.wet.add(left)
            if left + Loc2(0, 1) not in self._claywater_iter:
                new_sources.append(left)
                break
            left = left + Loc2(-1, 0)
        while right not in self.clay:
            self.wet.add(right)
            if right + Loc2(0, 1) not in self._claywater_iter:
                new_sources.append(right)
                break
            right = right + Loc2(1, 0)
        # print(left, right)

        # Make water
        if new_sources:
            for s in new_sources:
                self.active_spigots.append(s)
            return
        else:
            for x in range(left.x+1, right.x):
                self.water.add(Loc2(x, left.y))
            self.run_spigot(spigot)


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
    # input_str = test_input()
    reservoir = Reservoir(parse_input(input_str))
    x = 0
    while reservoir.active_spigots:
        x += 1
        print(x)
        if x >= 5:
            with open('reservoir/{}.txt'.format(x), 'w') as file:
                file.write('{}: {}\n'.format(x, str(reservoir.active_spigots)))
                file.write(str(reservoir))
        spigot = reservoir.active_spigots.pop(0)
        reservoir.run_spigot(spigot)
    return len(reservoir.wet.union(reservoir.water))


def part_2(input_str: str):
    return


def test_input():
    return textwrap.dedent("""\
    x=495, y=2..7
    y=7, x=495..501
    x=501, y=3..7
    x=498, y=2..4
    x=506, y=1..2
    x=498, y=10..13
    x=504, y=10..13
    y=13, x=498..504""")


def main():
    input_str = get_input(17)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
