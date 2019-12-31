from getinput import get_input
from pairs import dist_L1, Direction, add_pair, diag_adjacents
import itertools
import unittest


def get_coords(idx):
    n = 1
    while True:
        if n**2 > idx:
            break
        n += 2
    diff = n**2 - idx
    k = (n - 1) // 2
    # South side
    if (diff // (n-1)) == 0:
        return k - diff, -k
    # West side
    elif (diff // (n-1)) == 1:
        return -k, -k + (diff - (n-1))
    # North side
    elif (diff // (n-1)) == 2:
        return -k + (diff - 2*(n-1)), k
    # East side
    elif (diff // (n-1)) == 3:
        return k, k - (diff - 3*(n-1))


def sum_adjacent(loc, spiral):
    total = 0
    for offset in diag_adjacents:
        neighbor = add_pair(loc, offset)
        if neighbor in spiral:
            total += spiral[neighbor]
    return total


def part_1(square):
    return dist_L1((0, 0), get_coords(square))


def get_first_higher_than(square):
    depth = 1
    spiral = {(0, 0): 1}
    while True:
        # Go up
        for y in range(-depth+1, depth+1):
            val = sum_adjacent((depth, y), spiral)
            if val > square:
                return val, spiral
            spiral[(depth, y)] = val
        # Go left
        for x in range(depth-1, -(depth+1), -1):
            val = sum_adjacent((x, depth), spiral)
            if val > square:
                return val, spiral
            spiral[(x, depth)] = val
        # Go down
        for y in range(depth-1, -(depth+1), -1):
            val = sum_adjacent((-depth, y), spiral)
            if val > square:
                return val, spiral
            spiral[(-depth, y)] = val
        # Go right
        for x in range(-depth+1, depth+1):
            val = sum_adjacent((x, -depth), spiral)
            if val > square:
                return val, spiral
            spiral[(x, -depth)] = val
        depth += 1


def part_2(square):
    return get_first_higher_than(square)[0]


def main():
    input_str = int(get_input(3))
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


class TestSpiral(unittest.TestCase):
    def test_get_coords(self):
        self.assertEqual((1, 1), (get_coords(3)))
        self.assertEqual((-1, 2), get_coords(16))
        self.assertEqual((-2, -2), get_coords(21))


if __name__ == "__main__":
    main()
