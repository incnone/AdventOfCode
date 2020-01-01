from getinput import get_input
import itertools
from pairs import Direction, add_dir, add_pair
import string


class Path(object):
    def __init__(self, s):
        self.arr = list(list(c for c in line) for line in s.splitlines(keepends=False))

    def at(self, x, y):
        try:
            return self.arr[y][x]
        except IndexError:
            return ' '

    def start(self):
        for x in range(len(self.arr[0])):
            if self.arr[0][x] == '|':
                return x, 0


def both_parts(input_str):
    turn_vals = {
        Direction.NORTH: ([Direction.EAST, Direction.WEST], '-'),
        Direction.SOUTH: ([Direction.EAST, Direction.WEST], '-'),
        Direction.EAST: ([Direction.NORTH, Direction.SOUTH], '|'),
        Direction.WEST: ([Direction.NORTH, Direction.SOUTH], '|'),
    }

    path = Path(input_str)
    loc = path.start()
    direction = Direction.SOUTH
    letters = ''
    steps = 0

    while True:
        current = path.at(*loc)

        # If we're standing on empty space, time to end
        if current == ' ':
            return letters, steps

        # Mark any letters
        if current in string.ascii_uppercase:
            letters += current

        # If we're standing on a turn, change direction
        elif current == '+':
            turn_dirs, valid_char = turn_vals[direction]
            for d in turn_dirs:
                if path.at(*add_dir(loc, d)) == valid_char:
                    direction = d

        # Move once
        loc = add_dir(loc, direction)
        steps += 1


def main():
    input_str = get_input(19)
    part_1, part_2 = both_parts(input_str)
    print('Part 1:', part_1)
    print('Part 2:', part_2)


if __name__ == "__main__":
    main()
