from getinput import get_input
from util import grouper
import itertools
import textwrap
from enum import Enum


class InstructionType(Enum):
    TURN_ON = 0
    TURN_OFF = 1
    TOGGLE = 2


class LightGrid(object):
    _neighbor_pairs = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]

    def __init__(self, width, height):
        self.grid = list([[0 for _ in range(width)] for _ in range(height)])
        self.width = width
        self.height = height

    def __str__(self):
        return '\n'.join(''.join('#' if v else '.' for v in row) for row in self.grid)

    def at(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError
        return self.grid[y][x]

    def turn_on(self, x, y):
        self.grid[y][x] = 1

    def turn_off(self, x, y):
        self.grid[y][x] = 0

    def toggle(self, x, y):
        self.grid[y][x] = (self.grid[y][x] + 1) % 2

    def num_lit(self):
        return sum(v for row in self.grid for v in row)

    def num_lit_neighbors(self, x, y):
        num_lit = 0
        for offset in LightGrid._neighbor_pairs:
            try:
                num_lit += self.at(x+offset[0], y+offset[1])
            except IndexError:
                pass
        return num_lit

    def step(self):
        to_modify = dict()
        for x, y in itertools.product(range(self.width), range(self.height)):
            num_lit_neighbors = self.num_lit_neighbors(x, y)
            if self.at(x, y) == 1 and num_lit_neighbors not in [2, 3]:
                to_modify[(x, y)] = 0
            elif self.at(x, y) == 0 and num_lit_neighbors == 3:
                to_modify[(x, y)] = 1
        for loc, val in to_modify.items():
            self.grid[loc[1]][loc[0]] = val


def parse_input(big_str):
    light_grid = LightGrid(100, 100)
    for y, line in enumerate(big_str.splitlines(keepends=False)):
        for x, c in enumerate(line):
            if c == '#':
                light_grid.turn_on(x, y)
    return light_grid


def part_1(grid_str):
    light_grid = parse_input(grid_str)
    for _ in range(100):
        light_grid.step()
    return light_grid.num_lit()


def part_2(grid_str):
    light_grid = parse_input(grid_str)
    for x, y in [(0, 0), (0, 99), (99, 0), (99, 99)]:
        light_grid.turn_on(x, y)

    for _ in range(100):
        light_grid.step()
        for x, y in [(0, 0), (0, 99), (99, 0), (99, 99)]:
            light_grid.turn_on(x, y)

    return light_grid.num_lit()


if __name__ == "__main__":
    big_str = get_input(day=18)

    print('Part 1:', part_1(big_str))
    print('Part 2:', part_2(big_str))
