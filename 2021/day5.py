import textwrap
import itertools
import numpy as np
from typing import Optional, Tuple


def get_test_input() -> str:
    return textwrap.dedent("""\
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2""")


# class Line(object):
#     def __init__(self, s):
#         val1, val2 = s.split('->')
#         start = tuple(int(x) for x in val1.split(','))
#         end = tuple(int(x) for x in val2.split(','))
#         self.coeffs = sp.Matrix([[end[1]-start[1], start[0]-end[0],
#                                 (end[1]-start[1])*start[0] + (start[0]-end[0])*start[1]]])
#
#     def __str__(self):
#         return f'{self.coeffs[0]}x + {self.coeffs[1]}y = {self.coeffs[2]}'
#
#     def __repr__(self):
#         return str(self)
#
#     def intersection(self, other) -> Optional[Tuple[int]]:
#         mat = sp.Matrix([self.coeffs, other.coeffs])
#         red, piv = mat.rref()
#
#         if piv == (0,1):    # intersection is a point
#             point = tuple(mat.col(2))
#             if point[0].is_integer() and point[1].is_integer():
#                 return point
#             else:
#                 return None
#
#         elif piv == (0,):   # intersection is a vertical line
#
#         elif piv == (1,):   # intersection is a horizontal line
#
#         else:
#             return None


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


class Line(object):
    def __init__(self, s):
        val1, val2 = s.split('->')
        self.start = np.array(tuple(int(x) for x in val1.split(',')))
        self.end = np.array(tuple(int(x) for x in val2.split(',')))

    def __str__(self):
        return f'{self.start} -> {self.end}'

    def __repr__(self):
        return str(self)

    def fill_grid(self, grid):
        if self.start[0] == self.end[0]:
            miny = min(self.start[1], self.end[1])
            maxy = max(self.start[1], self.end[1])
            for y in range(miny, maxy+1, 1):
                grid[y][self.start[0]] += 1
        elif self.start[1] == self.end[1]:
            minx = min(self.start[0], self.end[0])
            maxx = max(self.start[0], self.end[0])
            for x in range(minx, maxx+1, 1):
                grid[self.start[1]][x] += 1
        else:
            xstep = sign(self.end[0] - self.start[0])
            ystep = sign(self.end[1] - self.start[1])
            for x, y in zip(range(self.start[0], self.end[0]+xstep, xstep),
                            range(self.start[1], self.end[1]+ystep, ystep)):
                grid[y][x] += 1


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = np.zeros((1000, 1000))
    for line in s.splitlines():
        Line(line).fill_grid(data)
    return data


def part_1(data):
    tot = 0
    for row in data:
        #print(row)
        for val in row:
            if val > 1:
                tot += 1
    print(f'Part 1: {tot}')


def part_2(data):
    pass


def main():
    data = read_input(day_number=5, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
