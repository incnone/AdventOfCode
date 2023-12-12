import textwrap
import numpy as np
from enum import Enum
from itertools import product


def get_test_input() -> str:
    return textwrap.dedent("""\
    FF7S7F7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-
    L---JF-JLJ.||-FJLJJ7
    |F|F-JF---7F7-L7L|7|
    |FFJF7L7F-JF7|JL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input(), test)
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read(), test)


class PipeType(Enum):
    NONE = 0
    VERT = 1
    HORIZ = 2
    BEND_L = 3
    BEND_J = 4
    BEND_7 = 5
    BEND_F = 6
    INSIDE = 7


def get_pipetype(c: str, test):
    if c == '.':
        return PipeType.NONE
    elif c == '|':
        return PipeType.VERT
    elif c == '-':
        return PipeType.HORIZ
    elif c == 'L':
        return PipeType.BEND_L
    elif c == 'J':
        return PipeType.BEND_J
    elif c == '7':
        return PipeType.BEND_7
    elif c == 'F':
        return PipeType.BEND_F
    elif c == 'S':
        return PipeType.BEND_F if test else PipeType.VERT    # by inspection


def pipelet(p):
    if p == PipeType.NONE:
        return '.'
    elif p == PipeType.VERT:
        return '|'
    elif p == PipeType.HORIZ:
        return '-'
    elif p == PipeType.BEND_L:
        return 'L'
    elif p == PipeType.BEND_J:
        return 'J'
    elif p == PipeType.BEND_7:
        return '7'
    elif p == PipeType.BEND_F:
        return 'F'
    elif p == PipeType.INSIDE:
        return 'I'
    return None


def parse_input(s: str, test):
    lines = list(s.splitlines(keepends=False))
    width = len(lines[0])
    height = len(lines)

    pipes = np.zeros((width, height), dtype=np.int8)
    startloc = None
    for x, y in product(range(width), range(height)):
        c = lines[y][x]
        if c == 'S':
            startloc = (x, y)
        pipes[x, y] = get_pipetype(c, test).value

    return pipes, startloc


def left(t):
    return t[0] - 1, t[1]


def right(t):
    return t[0] + 1, t[1]


def up(t):
    return t[0], t[1] - 1


def down(t):
    return t[0], t[1] + 1


def next_pipeloc(loc, last_loc, pipetype):
    if pipetype == PipeType.VERT:
        return down(loc) if last_loc == up(loc) else up(loc)
    elif pipetype == PipeType.HORIZ:
        return right(loc) if last_loc == left(loc) else left(loc)
    elif pipetype == PipeType.BEND_F:
        return right(loc) if last_loc == down(loc) else down(loc)
    elif pipetype == PipeType.BEND_7:
        return left(loc) if last_loc == down(loc) else down(loc)
    elif pipetype == PipeType.BEND_J:
        return left(loc) if last_loc == up(loc) else up(loc)
    elif pipetype == PipeType.BEND_L:
        return right(loc) if last_loc == up(loc) else up(loc)
    else:
        raise RuntimeError("Bad Pipetype for next_pipeloc")


def part_1(pipes, startloc):
    distance = np.zeros(pipes.shape)
    current_dist = 1
    loc_1 = startloc
    loc_2 = startloc
    prev_1 = startloc
    prev_2 = startloc

    starttype = PipeType(pipes[startloc])
    if starttype == PipeType.BEND_F:
        loc_1 = right(startloc)
        loc_2 = down(startloc)
    elif starttype == PipeType.BEND_7:
        loc_1 = left(startloc)
        loc_2 = down(startloc)
    elif starttype == PipeType.VERT:
        loc_1 = up(startloc)
        loc_2 = down(startloc)
    else:
        raise RuntimeError("Unsupported start type")

    while loc_1 != loc_2:
        distance[loc_1], distance[loc_2] = current_dist, current_dist
        temp_1, temp_2 = loc_1, loc_2
        loc_1, loc_2 = next_pipeloc(loc_1, prev_1, PipeType(pipes[loc_1])), next_pipeloc(loc_2, prev_2, PipeType(pipes[loc_2]))
        prev_1, prev_2 = temp_1, temp_2
        current_dist += 1

    print(f'Part 1: {current_dist}')


def print_pipe(pipes):
    return '\n'.join(
        ''.join(pipelet(PipeType(pipes[x, y])) for x in range(pipes.shape[0]))
        for y in range(pipes.shape[1])
    )


def part_2(pipes, startloc):
    realpipe = np.zeros(pipes.shape, dtype=np.int8)
    current_dist = 1
    loc_1 = startloc
    loc_2 = startloc
    prev_1 = startloc
    prev_2 = startloc

    starttype = PipeType(pipes[startloc])
    if starttype == PipeType.BEND_F:
        loc_1 = right(startloc)
        loc_2 = down(startloc)
    elif starttype == PipeType.BEND_7:
        loc_1 = left(startloc)
        loc_2 = down(startloc)
    elif starttype == PipeType.VERT:
        loc_1 = up(startloc)
        loc_2 = down(startloc)
    else:
        raise RuntimeError("Unsupported start type")

    realpipe[startloc] = pipes[startloc]
    while loc_1 != loc_2:
        realpipe[loc_1], realpipe[loc_2] = pipes[loc_1], pipes[loc_2]
        temp_1, temp_2 = loc_1, loc_2
        loc_1, loc_2 = next_pipeloc(loc_1, prev_1, PipeType(pipes[loc_1])), \
                       next_pipeloc(loc_2, prev_2, PipeType(pipes[loc_2]))
        prev_1, prev_2 = temp_1, temp_2
        current_dist += 1
    realpipe[loc_1] = pipes[loc_1]

    num_inside = 0
    for y in range(realpipe.shape[1]):
        inside = False
        crossdir = 0
        for x in range(realpipe.shape[0]):
            thispipe = PipeType(realpipe[x, y])
            if thispipe == PipeType.NONE:
                num_inside += 1 if inside else 0
            elif thispipe == PipeType.VERT:
                inside = not inside
            elif thispipe == PipeType.BEND_F:
                crossdir = -1
            elif thispipe == PipeType.BEND_L:
                crossdir = 1
            elif thispipe == PipeType.BEND_7:
                inside = ((crossdir == 1) != inside)    # Swap whether we're inside if crossdir "changes"
            elif thispipe == PipeType.BEND_J:
                inside = ((crossdir == -1) != inside)

    print(f'Part 2: {num_inside}')


def main():
    pipes, startloc = read_input(day_number=10, test=False)
    part_1(pipes, startloc)
    part_2(pipes, startloc)


if __name__ == "__main__":
    main()
