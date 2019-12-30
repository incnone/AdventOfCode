from getinput import get_input
from util import grouper


def num_valid(triangles):
    num = 0
    for x, y, z in triangles:
        num += 1 if valid_triangle(x, y, z) else 0
    return num


def valid_triangle(x, y, z):
    return x + y > z and x + z > y and y + z > x


def part_1(s):
    triangles = []
    for line in s.splitlines(keepends=False):
        triangles.append(tuple(int(x) for x in line.split()))
    return num_valid(triangles)


def part_2(s):
    triangles = []
    for lns in grouper(s.splitlines(keepends=False), 3):
        split_lns = tuple(ln.split() for ln in lns)
        for idx in range(3):
            triangles.append(tuple(int(split_lns[jdx][idx]) for jdx in range(3)))
    return num_valid(triangles)


if __name__ == "__main__":
    the_big_str = get_input(3)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
