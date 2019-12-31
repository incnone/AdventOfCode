from enum import Enum
from typing import Tuple


diag_adjacents = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    @property
    def pair(self):
        if self == Direction.NORTH:
            return 0, -1
        elif self == Direction.SOUTH:
            return 0, 1
        elif self == Direction.WEST:
            return -1, 0
        elif self == Direction.EAST:
            return 1, 0

    @property
    def opposite(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.WEST:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.WEST


def add_pair(p1: Tuple[int, int], p2: Tuple[int, int]):
    return p1[0] + p2[0], p1[1] + p2[1]


def add_dir(p1: Tuple[int, int], p2: Direction):
    return add_pair(p1, p2.pair)


def dist_L1(p1: Tuple[int, int], p2: Tuple[int, int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
