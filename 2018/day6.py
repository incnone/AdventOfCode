from getinput import get_input
import textwrap
from grid import Loc2, Direction
from typing import Iterable
import itertools
from collections import defaultdict


def get_bounds(points: Iterable[Loc2]):
    i = iter(points)
    p = next(i)
    min_x = max_x = p.x
    min_y = max_y = p.y
    for p in i:
        min_x = min(min_x, p.x)
        max_x = max(max_x, p.x)
        min_y = min(min_y, p.y)
        max_y = max(max_y, p.y)
    return min_x, max_x, min_y, max_y


def dirs_from_origin(p):
    dirs = set()
    if abs(p.y) >= abs(p.x):
        if p.y > 0:
            dirs.add(Direction.SOUTH)
        elif p.y < 0:
            dirs.add(Direction.NORTH)
    if abs(p.x) >= abs(p.y):
        if p.x > 0:
            dirs.add(Direction.EAST)
        elif p.x < 0:
            dirs.add(Direction.WEST)
    return dirs


def has_finite_area(p: Loc2, points: Iterable[Loc2]):
    satisfied_dirs = set()
    for q in points:
        satisfied_dirs.update(dirs_from_origin(q - p))
    return len(satisfied_dirs) == 4


def nearest_points(p, points):
    i = iter(points)
    first = next(i)
    nearest = {first}
    min_distance = Loc2.dist_l1(p, first)
    for q in i:
        d = Loc2.dist_l1(p, q)
        if d == min_distance:
            nearest.add(q)
        elif d < min_distance:
            min_distance = d
            nearest = {q}
    return nearest, min_distance


def get_center_of_mass(points):
    com = sum(points, Loc2(0, 0))
    return Loc2(com.x // len(points), com.y // len(points))


def get_total_distance(p, points):
    return sum(Loc2.dist_l1(p, q) for q in points)


def parse_input(s):
    return list(Loc2(*(int(x) for x in line.split(','))) for line in s.splitlines(keepends=False))


def part_1(input_str):
    # input_str = test_input()

    points = parse_input(input_str)
    min_x, max_x, min_y, max_y = get_bounds(points)
    nearest_point = defaultdict(lambda: set())
    for x, y in itertools.product(range(min_x, max_x+1), range(min_y, max_y+1)):
        p = Loc2(x, y)
        nearest, dist = nearest_points(p, points)
        if len(nearest) == 1:
            nearest_point[next(iter(nearest))].add(p)
    return max(len(x) for x in nearest_point.values())


def part_2(input_str):
    # input_str = test_input()
    too_far = 10000

    points = parse_input(input_str)
    num_found = 0
    to_search = [get_center_of_mass(points)]
    searched = {to_search[0]}
    while to_search:
        p = to_search.pop()
        if get_total_distance(p, points) < too_far:
            num_found += 1
            for d in Direction:
                neighbor = p + d
                if neighbor not in searched:
                    searched.add(neighbor)
                    to_search.append(neighbor)
    return num_found


def test_input():
    return textwrap.dedent("""\
    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9""")


def main():
    input_str = get_input(6)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
