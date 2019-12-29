import itertools
import textwrap
from pairs import Direction, add_dir, add_pair
from enum import Enum


class LightGrid(object):
    _neighbor_pairs = [
        (0, -1),
        (-1, 0), (1, 0),
        (0, 1)
    ]
    # _neighbor_pairs = [
    #     (-1, -1), (0, -1), (1, -1),
    #     (-1, 0), (1, 0),
    #     (-1, 1), (0, 1), (1, 1)
    # ]

    def __init__(self, width, height):
        self.grid = list([[0 for _ in range(width)] for _ in range(height)])
        self.width = width
        self.height = height

    def __str__(self):
        return '\n'.join(''.join('#' if v else '.' for v in row) for row in self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return self.grid != other.grid

    def biodiversity(self):
        return sum(pow(2, idx) if gridval == 1 else 0 for idx, gridval in enumerate(itertools.chain(*self.grid)))

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
            if self.at(x, y) == 1 and num_lit_neighbors != 1:
                to_modify[(x, y)] = 0
            elif self.at(x, y) == 0 and num_lit_neighbors in [1, 2]:
                to_modify[(x, y)] = 1
        for loc, val in to_modify.items():
            self.grid[loc[1]][loc[0]] = val


class FractalBugGrid(object):
    def __init__(self):
        self.width = self.height = 5
        self.grid = list([[0 for _ in range(self.width)] for _ in range(self.height)])
        self.center = (2, 2)
        self.inner_grid = None
        self.outer_grid = None
        self.lifetime = 0

    def __str__(self):
        return '\n'.join(''.join('#' if v else '.' for v in row) for row in self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return self.grid != other.grid

    def num_bugs(self):
        return self._num_bugs_outward() + self._num_bugs_inward() + self._num_bugs_thislevel()

    def _num_bugs_thislevel(self):
        return sum(itertools.chain(*self.grid))

    def _num_bugs_outward(self):
        if self.outer_grid is None:
            return 0
        else:
            return self.outer_grid._num_bugs_thislevel() + self.outer_grid._num_bugs_outward()

    def _num_bugs_inward(self):
        if self.inner_grid is None:
            return 0
        else:
            return self.inner_grid._num_bugs_thislevel() + self.inner_grid._num_bugs_inward()

    def at(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError
        return self.grid[y][x]

    def outer_grid_at(self, x, y):
        return 0 if self.outer_grid is None else self.outer_grid.at(x, y)

    def inner_grid_at(self, x, y):
        return 0 if self.inner_grid is None else self.inner_grid.at(x, y)

    def adj_bugs(self, x, y, d):
        if x == 0 and d == Direction.WEST:
            return self.outer_grid_at(1, 2)
        elif y == 0 and d == Direction.NORTH:
            return self.outer_grid_at(2, 1)
        elif x == self.width-1 and d == Direction.EAST:
            return self.outer_grid_at(3, 2)
        elif y == self.height-1 and d == Direction.SOUTH:
            return self.outer_grid_at(2, 3)
        elif x == 1 and y == 2 and d == Direction.EAST:
            return sum(self.inner_grid_at(0, yp) for yp in range(self.height))
        elif x == 2 and y == 1 and d == Direction.SOUTH:
            return sum(self.inner_grid_at(xp, 0) for xp in range(self.width))
        elif x == 3 and y == 2 and d == Direction.WEST:
            return sum(self.inner_grid_at(self.width-1, yp) for yp in range(self.height))
        elif x == 2 and y == 3 and d == Direction.NORTH:
            return sum(self.inner_grid_at(xp, self.height-1) for xp in range(self.width))
        else:
            return self.at(*add_dir((x, y), d))

    def turn_on(self, x, y):
        self.grid[y][x] = 1

    def turn_off(self, x, y):
        self.grid[y][x] = 0

    def num_lit_neighbors(self, x, y):
        return sum(self.adj_bugs(x, y, d) for d in Direction)

    def step(self, step_outward=True, step_inward=True):
        if step_outward and self.outer_grid is None:
            self.outer_grid = FractalBugGrid()
            self.outer_grid.inner_grid = self
            self.outer_grid.lifetime = -2
        if step_inward and self.inner_grid is None:
            self.inner_grid = FractalBugGrid()
            self.inner_grid.outer_grid = self
            self.inner_grid.lifetime = -2

        to_modify = dict()
        for x, y in itertools.product(range(self.width), range(self.height)):
            if (x, y) == self.center:
                continue
            num_lit_neighbors = self.num_lit_neighbors(x, y)
            if self.at(x, y) == 1 and num_lit_neighbors != 1:
                to_modify[(x, y)] = 0
            elif self.at(x, y) == 0 and num_lit_neighbors in [1, 2]:
                to_modify[(x, y)] = 1

        if self.outer_grid is not None and step_outward and self.lifetime >= 0:
            self.outer_grid.step(step_inward=False, step_outward=True)
        if self.inner_grid is not None and step_inward and self.lifetime >= 0:
            self.inner_grid.step(step_inward=True, step_outward=False)

        for loc, val in to_modify.items():
            self.grid[loc[1]][loc[0]] = val
        self.lifetime += 1


def parse_input(big_str):
    light_grid = LightGrid(5, 5)
    for y, line in enumerate(big_str.splitlines(keepends=False)):
        for x, c in enumerate(line):
            if c == '#':
                light_grid.turn_on(x, y)
    print('{:b}'.format(light_grid.biodiversity()))
    return light_grid


def parse_input_2(big_str):
    bug_grid = FractalBugGrid()
    for y, line in enumerate(big_str.splitlines(keepends=False)):
        for x, c in enumerate(line):
            if c == '#':
                bug_grid.turn_on(x, y)
    return bug_grid


def test():
    light_grid = parse_input(textwrap.dedent("""\
    ....#
    #..#.
    #..##
    ..#..
    #...."""))
    for step in range(5):
        print(step)
        print(light_grid)
        light_grid.step()


def part_1(big_str):
    light_grid = parse_input(big_str)
    biodiversities = set()
    while light_grid.biodiversity() not in biodiversities:
        biodiversities.add(light_grid.biodiversity())
        light_grid.step()
    return light_grid.biodiversity()


def part_2(grid_str):
    bug_grid = parse_input_2(grid_str)
    for _ in range(200):
        bug_grid.step()
    return bug_grid.num_bugs()


if __name__ == "__main__":
    with open('input/dec24.txt', 'r') as file:
        the_big_str = file.read()

    test_str = textwrap.dedent("""\
    ....#
    #..#.
    #..##
    ..#..
    #....""")

    # print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
