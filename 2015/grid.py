"""Convenience methods for dealing with pairs of ints"""
import unittest
from enum import Enum


class Loc2(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __setattr__(self, *ignored):
        raise NotImplementedError

    def __delattr__(self, *ignored):
        raise NotImplementedError

    def __add__(self, other):
        return Loc2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Loc2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Loc2(-self.x, -self.y)

    def __iadd__(self, other):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError


class Direction(Enum):
    NORTH = 0
    WEST = 1
    EAST = 2
    SOUTH = 3

    @property
    def pair(self):
        if self == Direction.NORTH:
            return Loc2(0, -1)
        elif self == Direction.WEST:
            return Loc2(-1, 0)
        elif self == Direction.EAST:
            return Loc2(1, 0)
        elif self == Direction.SOUTH:
            return Loc2(0, 1)

    @property
    def x(self):
        return self.pair[0]

    @property
    def y(self):
        return self.pair[1]


class TestLoc(unittest.TestCase):
    def test_create(self):
        loc = Loc2(5, 15)
        self.assertEqual('(5, 15)', str(loc))

    def test_add(self):
        self.assertEqual(Loc2(2, 3), Loc2(5, 6) + Loc2(-3, -3))
        self.assertEqual(Loc2(2, 3), Loc2(5, 6) - Loc2(3, 3))

    def test_neg(self):
        self.assertEqual(-Loc2(2, 3), Loc2(-2, -3))


class TestDir(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Loc2(2, 3), Loc2(2, 2) + Direction.SOUTH)
