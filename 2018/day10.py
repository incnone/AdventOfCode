from getinput import get_input
import textwrap
from grid import Loc2
import re
from typing import Iterable


class Point(object):
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return 'P(p={}, v={})'.format(self.pos, self.vel)

    def __repr__(self):
        return 'P(p={}, v={})'.format(self.pos, self.vel)

    def tick(self):
        self.pos = self.pos + self.vel


def get_bounds(points: Iterable[Point]):
    min_x = max_x = min_y = max_y = None
    for p in points:
        min_x = min(p.pos.x, min_x) if min_x is not None else p.pos.x
        max_x = max(p.pos.x, max_x) if max_x is not None else p.pos.x
        min_y = min(p.pos.y, min_y) if min_y is not None else p.pos.y
        max_y = max(p.pos.y, max_y) if max_y is not None else p.pos.y
    return min_x, max_x, min_y, max_y


def print_points(points: Iterable[Point]):
    min_x, max_x, min_y, max_y = get_bounds(points)
    point_locs = set()
    for p in points:
        point_locs.add(p.pos)

    return '\n'.join(
        ''.join('#' if Loc2(x, y) in point_locs else ' ' for x in range(min_x, max_x+1))
        for y in range(min_y, max_y+1)
    )


def parse_input(s: str):
    points = []
    for line in s.splitlines(keepends=False):
        pos = Loc2(*[int(x) for x in re.findall(r'position=<(-*\W*\d+, -*\W*\d+)>', line)[0].split(',')])
        vel = Loc2(*[int(x) for x in re.findall(r'velocity=<(-*\W*\d+, -*\W*\d+)>', line)[0].split(',')])
        points.append(Point(pos=pos, vel=vel))
    return points


def both_parts(input_str: str):
    # input_str = test_input()
    points = parse_input(input_str)
    has_been_close = False
    close = False
    seconds = 0
    while close or not has_been_close:
        min_x, max_x, min_y, max_y = get_bounds(points)
        close = (max_y - min_y) < 10
        has_been_close = has_been_close or close
        if close:
            return '\n' + print_points(points), str(seconds)
        for p in points:
            p.tick()
        seconds += 1
    return


def test_input():
    return textwrap.dedent("""\
    position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>""")


def main():
    input_str = get_input(10)
    part_1, part_2 = both_parts(input_str)
    print('Part 1:', part_1)
    print('Part 2:', part_2)


if __name__ == "__main__":
    main()
