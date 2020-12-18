import itertools
import textwrap
from typing import Set, Tuple


class ConwayCube(object):
    _neighbor_offsets = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                if x != 0 or y != 0 or z != 0:
                    _neighbor_offsets.append((x, y, z))

    def __init__(self, s):
        self.active_cubes = set()       # type: Set[Tuple[int, int, int]]
        for y, line in enumerate(reversed(s.splitlines())):
            for x, c in enumerate(line.rstrip('\n')):
                if c == '#':
                    self.active_cubes.add((x, y, 0))
        self.bounds_x = None
        self.bounds_y = None
        self.bounds_z = None
        self._set_bounds()

    def _set_bounds(self):
        self.bounds_x = (min(x[0] for x in self.active_cubes), max(x[0] for x in self.active_cubes) + 1)
        self.bounds_y = (min(x[1] for x in self.active_cubes), max(x[1] for x in self.active_cubes) + 1)
        self.bounds_z = (min(x[2] for x in self.active_cubes), max(x[2] for x in self.active_cubes) + 1)

    def _slice_str(self, z):
        return '\n'.join(
            ''.join(self[(x, y, z)] for x in range(self.bounds_x[0], self.bounds_x[1]))
            for y in reversed(range(self.bounds_y[0], self.bounds_y[1]))
        )

    def __getitem__(self, item: Tuple[int, int, int]):
        return '#' if item in self.active_cubes else '.'

    def __iter__(self):
        for x, y, z in itertools.product(
                range(self.bounds_x[0]-1, self.bounds_x[1]+1),
                range(self.bounds_y[0]-1, self.bounds_y[1]+1),
                range(self.bounds_z[0]-1, self.bounds_z[1]+1),
        ):
            yield (x, y, z)

    def __str__(self):
        return '\n\n'.join(
            f'z={z}\n{self._slice_str(z)}'
            for z in range(self.bounds_z[0], self.bounds_z[1])
        )

    @property
    def num_active(self):
        return len(self.active_cubes)

    @staticmethod
    def neighbors(loc):
        return [(loc[0] + off[0], loc[1] + off[1], loc[2] + off[2]) for off in ConwayCube._neighbor_offsets]

    def num_active_neighbors(self, loc):
        return sum(1 if n in self.active_cubes else 0 for n in ConwayCube.neighbors(loc))

    def step(self):
        new_active = set()
        for v in self:
            active_neighbors = self.num_active_neighbors(v)
            if (self[v] == '#' and 2 <= active_neighbors <= 3) or (self[v] == '.' and active_neighbors == 3):
                new_active.add(v)
        self.active_cubes = new_active
        self._set_bounds()


class ConwayHypercube(object):
    _neighbor_offsets = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                for w in range(-1, 2):
                    if x != 0 or y != 0 or z != 0 or w != 0:
                        _neighbor_offsets.append((x, y, z, w))

    def __init__(self, s):
        self.active_cubes = set()       # type: Set[Tuple[int, int, int, int]]
        for y, line in enumerate(reversed(s.splitlines())):
            for x, c in enumerate(line.rstrip('\n')):
                if c == '#':
                    self.active_cubes.add((x, y, 0, 0))
        self.bounds_x = None
        self.bounds_y = None
        self.bounds_z = None
        self.bounds_w = None
        self._set_bounds()

    def _set_bounds(self):
        if not self.active_cubes:
            self.bounds_x = self.bounds_y = self.bounds_z = self.bounds_w = (0, 0)
            print('Warning: Empty Conway Hypercube.')
            return
        self.bounds_x = (min(x[0] for x in self.active_cubes), max(x[0] for x in self.active_cubes) + 1)
        self.bounds_y = (min(x[1] for x in self.active_cubes), max(x[1] for x in self.active_cubes) + 1)
        self.bounds_z = (min(x[2] for x in self.active_cubes), max(x[2] for x in self.active_cubes) + 1)
        self.bounds_w = (min(x[3] for x in self.active_cubes), max(x[3] for x in self.active_cubes) + 1)

    def _slice_str(self, z, w):
        return '\n'.join(
            ''.join(self[(x, y, z, w)] for x in self._xrange)
            for y in reversed(self._yrange)
        )

    @property
    def _xrange(self):
        return range(self.bounds_x[0], self.bounds_x[1])

    @property
    def _yrange(self):
        return range(self.bounds_y[0], self.bounds_y[1])

    @property
    def _zrange(self):
        return range(self.bounds_z[0], self.bounds_z[1])

    @property
    def _wrange(self):
        return range(self.bounds_w[0], self.bounds_w[1])

    def __getitem__(self, item: Tuple[int, int, int, int]):
        return '#' if item in self.active_cubes else '.'

    def __iter__(self):
        for x, y, z, w in itertools.product(
                range(self.bounds_x[0] - 1, self.bounds_x[1] + 1),
                range(self.bounds_y[0] - 1, self.bounds_y[1] + 1),
                range(self.bounds_z[0] - 1, self.bounds_z[1] + 1),
                range(self.bounds_w[0] - 1, self.bounds_w[1] + 1),
        ):
            yield (x, y, z, w)

    def __str__(self):
        return '\n\n'.join(
            f'z={z}, w={w}\n{self._slice_str(z, w)}'
            for w, z in itertools.product(self._wrange, self._zrange)
        )

    @property
    def num_active(self):
        return len(self.active_cubes)

    @staticmethod
    def neighbors(loc):
        return [
            (loc[0] + off[0], loc[1] + off[1], loc[2] + off[2], loc[3] + off[3])
            for off in ConwayHypercube._neighbor_offsets
        ]

    def num_active_neighbors(self, loc):
        return sum(1 if n in self.active_cubes else 0 for n in ConwayHypercube.neighbors(loc))

    def step(self):
        new_active = set()
        for v in self:
            active_neighbors = self.num_active_neighbors(v)
            # print(f'{v} ({self[v]}) has {active_neighbors} active neighbors.')
            if (self[v] == '#' and 2 <= active_neighbors <= 3) or (self[v] == '.' and active_neighbors == 3):
                new_active.add(v)
        self.active_cubes = new_active
        self._set_bounds()


def get_test_input() -> str:
    return textwrap.dedent("""\
    .#.
    ..#
    ###""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return s


def part_1(s):
    data = ConwayCube(s)
    for _ in range(6):
        data.step()
    print('Part 1:', data.num_active)


def part_2(s):
    data = ConwayHypercube(s)
    for _ in range(6):
        data.step()
    print('Part 2:', data.num_active)


def main():
    s = read_input(day_number=17, test=False)
    # part_1(s)
    part_2(s)


if __name__ == "__main__":
    main()
