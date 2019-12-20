from getinput import get_input
from grid import Loc2, Direction
from util import grouper


def get_dir(c):
    if c == '^':
        return Direction.NORTH
    elif c == 'v':
        return Direction.SOUTH
    elif c == '<':
        return Direction.WEST
    elif c == '>':
        return Direction.EAST
    else:
        return None


def inputs_to_dirs(inputstr):
    dirs = []
    for c in inputstr:
        dirs.append(get_dir(c))
    return dirs


class RoboSanta(object):
    def __init__(self):
        self.current_loc = Loc2(0, 0)
        self.visited = {self.current_loc}

    def move(self, d):
        self.current_loc = self.current_loc + d
        self.visited.add(self.current_loc)


def part_1(dirs):
    current_loc = Loc2(0, 0)
    visited = {current_loc}
    for d in dirs:
        current_loc = current_loc + d
        visited.add(current_loc)
    return len(visited)


def part_2(dirs):
    santa = RoboSanta()
    robosanta = RoboSanta()
    for d1, d2 in grouper(dirs, 2):
        santa.move(d1)
        robosanta.move(d2)

    return len(santa.visited.union(robosanta.visited))


if __name__ == "__main__":
    dirs = inputs_to_dirs(get_input(3))

    print('Part 1:', part_1(dirs))
    print('Part 2:', part_2(dirs))
