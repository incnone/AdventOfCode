from getinput import get_input
import itertools
from collections import defaultdict
from pairs import Direction, add_pair, add_dir
import textwrap
from enum import Enum


class VirusCarrier(object):
    def __init__(self, loc):
        self.loc = loc
        self.dir = Direction.NORTH


class GridCluster(object):
    @staticmethod
    def get_infected_from_str(s):
        infected = defaultdict(lambda: False)
        # Find string center
        lines = s.splitlines(keepends=False)
        width = len(lines[0])
        height = len(lines)
        assert width % 2 == height % 2 == 1
        neg_center = (-(width // 2), -(height // 2))
        for jdx, line in enumerate(lines):
            for idx, c in enumerate(line):
                coord = add_pair((idx, jdx), neg_center)
                infected[coord] = c == '#'
        return infected

    def __init__(self, s):
        self.infected = self.get_infected_from_str(s)
        self.carrier = VirusCarrier((0, 0))
        self.infected_bursts = 0

    def __str__(self):
        x_bds = [9999999, -9999999]
        y_bds = [9999999, -9999999]
        for x, y in self.infected.keys():
            x_bds[0] = min(x_bds[0], x)
            x_bds[1] = max(x_bds[1], x)
            y_bds[0] = min(y_bds[0], y)
            y_bds[1] = max(y_bds[1], y)

        return '\n'.join(
            ''.join('#' if self.infected[(x, y)] else '.' for x in range(x_bds[0], x_bds[1]+1))
            for y in range(y_bds[0], y_bds[1]+1)
        )

    def burst(self):
        self.carrier.dir = self.carrier.dir.right if self.infected[self.carrier.loc] else self.carrier.dir.left
        self.infected[self.carrier.loc] = not self.infected[self.carrier.loc]
        if self.infected[self.carrier.loc]:
            self.infected_bursts += 1
        self.carrier.loc = add_dir(self.carrier.loc, self.carrier.dir)


class ComplicatedGridCluster(object):
    @staticmethod
    def get_infected_from_str(s):
        infected = defaultdict(lambda: 0)
        # Find string center
        lines = s.splitlines(keepends=False)
        width = len(lines[0])
        height = len(lines)
        assert width % 2 == height % 2 == 1
        neg_center = (-(width // 2), -(height // 2))
        for jdx, line in enumerate(lines):
            for idx, c in enumerate(line):
                coord = add_pair((idx, jdx), neg_center)
                infected[coord] = 2 if c == '#' else 0
        return infected

    inf_char_dict = {
        0: '.',
        1: 'W',
        2: '#',
        3: 'F'
    }

    def __init__(self, s):
        self.infected = self.get_infected_from_str(s)
        self.carrier = VirusCarrier((0, 0))
        self.infected_bursts = 0

    def __str__(self):
        x_bds = [9999999, -9999999]
        y_bds = [9999999, -9999999]
        for x, y in self.infected.keys():
            x_bds[0] = min(x_bds[0], x)
            x_bds[1] = max(x_bds[1], x)
            y_bds[0] = min(y_bds[0], y)
            y_bds[1] = max(y_bds[1], y)

        return '\n'.join(
            ''.join(ComplicatedGridCluster.inf_char_dict[self.infected[(x, y)]] for x in range(x_bds[0], x_bds[1]+1))
            for y in range(y_bds[0], y_bds[1]+1)
        )

    def burst(self):
        infection_state = self.infected[self.carrier.loc]
        if infection_state == 0:
            self.carrier.dir = self.carrier.dir.left
        elif infection_state == 1:
            self.infected_bursts += 1
        elif infection_state == 2:
            self.carrier.dir = self.carrier.dir.right
        elif infection_state == 3:
            self.carrier.dir = self.carrier.dir.opposite

        self.infected[self.carrier.loc] = (infection_state + 1) % 4
        self.carrier.loc = add_dir(self.carrier.loc, self.carrier.dir)


def test_input():
    return textwrap.dedent("""\
    ..#
    #..
    ...""")


def part_1(input_str):
    grid = GridCluster(input_str)
    for x in range(10000):
        grid.burst()
    return grid.infected_bursts


def part_2(input_str):
    # Takes a couple minutes
    grid = ComplicatedGridCluster(input_str)
    for x in range(10000000):
        grid.burst()
    return grid.infected_bursts


def main():
    input_str = get_input(22)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
