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
    def right(self):
        right_dir = {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
            Direction.EAST: Direction.SOUTH
        }
        return right_dir[self]

    @property
    def left(self):
        left_dir = {
            Direction.NORTH: Direction.WEST,
            Direction.SOUTH: Direction.EAST,
            Direction.WEST: Direction.SOUTH,
            Direction.EAST: Direction.NORTH
        }
        return left_dir[self]

    @property
    def pair(self):
        pair_dir = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
            Direction.EAST: (1, 0)
        }
        return pair_dir[self]

    @property
    def opposite(self):
        opposite_dir = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST
        }
        return opposite_dir[self]


def add_pair(p1: Tuple[int, int], p2: Tuple[int, int]):
    return p1[0] + p2[0], p1[1] + p2[1]


def add_dir(p1: Tuple[int, int], p2: Direction):
    return add_pair(p1, p2.pair)


def neg(p: Tuple[int, int]):
    return -p[0], -p[1]


def dist_L1(p1: Tuple[int, int], p2: Tuple[int, int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
