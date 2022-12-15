import textwrap
import math
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        pairs = line.split(' -> ')
        path = []
        for p in pairs:
            x = p.split(',')
            path.append((int(x[0]), int(x[1])))
        data.append(path)
    return data


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


class RockWall(object):
    def __init__(self, walls, has_bottom):
        self.minx = min(min(p[0] for p in path) for path in walls) - 500
        self.maxx = max(max(p[0] for p in path) for path in walls) + 500
        self.miny = 0  # min(min(p[1] for p in path) for path in walls)
        self.maxy = max(max(p[1] for p in path) for path in walls) + (1 if has_bottom else 0)
        self.area = np.zeros((self.maxy - self.miny + 1, self.maxx - self.minx + 1))
        self.full = False
        self.num_sand = 0
        self.has_bottom = has_bottom

        for path in walls:
            for idx in range(len(path) - 1):
                p1, p2 = path[idx], path[idx+1]
                if p1[0] == p2[0]:
                    sgn = sign(p2[1] - p1[1])
                    for y in range(p1[1], p2[1] + sgn, sgn):
                        self.area[self.coord((p1[0], y))] = 1
                else:
                    sgn = sign(p2[0] - p1[0])
                    for x in range(p1[0], p2[0] + sgn, sgn):
                        self.area[self.coord((x, p1[1]))] = 1

    def __str__(self):
        chars = {
            0: '.',
            1: '#',
            2: 'o'
        }
        return '\n'.join(''.join(chars[c] for c in row) for row in self.area)

    def coord(self, t):
        return t[1] - self.miny, t[0] - self.minx

    def make_sand(self):
        new_sand = np.array(self.coord((500, 0)))
        moved = True
        while moved:
            moved = False
            for disp in [np.array([1, 0]), np.array([1, -1]), np.array([1, 1])]:
                new_loc = new_sand + disp
                if new_loc[0] > self.maxy:
                    if not self.has_bottom:
                        self.full = True
                    break

                if self.area[tuple(new_loc)] == 0:
                    new_sand += disp
                    moved = True
                    break

        if not self.full:
            nst = tuple(new_sand)
            if nst == self.coord(np.array([500, 0])):
                self.full = True

            self.area[tuple(new_sand)] = 2
            self.num_sand += 1


def part_1(data):
    wall = RockWall(data, has_bottom=False)
    while not wall.full:
        wall.make_sand()
    print(f'Part 1: {wall.num_sand}')


def part_2(data):
    wall = RockWall(data, has_bottom=True)
    while not wall.full:
        wall.make_sand()
    print(f'Part 2: {wall.num_sand}')


def main():
    data = read_input(day_number=14, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
