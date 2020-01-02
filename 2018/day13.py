from getinput import get_input
import itertools
import textwrap
from enum import Enum
from grid import Loc2, Direction, Loc2Grid


class CartCrashError(Exception):
    def __init__(self, loc, *args):
        Exception.__init__(self, *args)
        self.loc = loc


class MineCart(object):
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
        self.turn_index = 0

    def __repr__(self):
        return 'Cart({}, {})'.format(self.loc, self.dir)

    def move(self, trackpiece):
        # Handle turning
        if trackpiece in ['-', '|']:
            pass
        elif trackpiece == '+':
            if self.turn_index == 0:
                self.dir = self.dir.left
            elif self.turn_index == 2:
                self.dir = self.dir.right
            self.turn_index = (self.turn_index + 1) % 3
        elif trackpiece == '\\':
            turns = {
                Direction.NORTH: Direction.WEST,
                Direction.WEST: Direction.NORTH,
                Direction.EAST: Direction.SOUTH,
                Direction.SOUTH: Direction.EAST
            }
            self.dir = turns[self.dir]
        elif trackpiece == '/':
            turns = {
                Direction.NORTH: Direction.EAST,
                Direction.EAST: Direction.NORTH,
                Direction.WEST: Direction.SOUTH,
                Direction.SOUTH: Direction.WEST
            }
            self.dir = turns[self.dir]

        # Go forward
        self.loc = self.loc + self.dir


class MineTrack(object):
    def __init__(self, tracks, carts):
        self.tracks = tracks
        self.carts = carts
        self.crashes = []

    def __str__(self):
        return '\n'.join(
            ''.join(self._str_char(x, y) for x in range(len(line)))
            for y, line in enumerate(self.tracks.arr)
        )

    def _str_char(self, x, y):
        cart_chars = {
            Direction.NORTH: '^',
            Direction.EAST: '>',
            Direction.WEST: '<',
            Direction.SOUTH: 'v'
        }

        for cart in self.carts:
            if cart.loc == Loc2(x, y):
                return cart_chars[cart.dir]
        return self.tracks.at(Loc2(x, y))

    def advance_carts(self):
        self.carts = list(sorted(self.carts, key=lambda c: (c.loc.y, c.loc.x)))
        carts_to_remove = []
        for cart in self.carts:
            if cart in carts_to_remove:
                continue
            cart.move(trackpiece=self.tracks.at(cart.loc))
            for other_cart in self.carts:
                if other_cart != cart and other_cart not in carts_to_remove and other_cart.loc == cart.loc:
                    carts_to_remove += [cart, other_cart]
                    self.crashes.append(cart.loc)
        for cart in carts_to_remove:
            self.carts.remove(cart)

    def get_crash_loc(self):
        for cart_1, cart_2 in itertools.combinations(self.carts, 2):
            if cart_1.loc == cart_2.loc:
                return cart_1.loc
        return None


def parse_input(s: str):
    convert_char = {
        '-': '-',
        '|': '|',
        '+': '+',
        '\\': '\\',
        '/': '/',
        '^': '|',
        '>': '-',
        '<': '-',
        'v': '|',
        ' ': ' '
    }

    cart_dirs = {
        '^': Direction.NORTH,
        '>': Direction.EAST,
        '<': Direction.WEST,
        'v': Direction.SOUTH
    }

    tracks = Loc2Grid(arr=list(list(convert_char[c] for c in line) for line in s.splitlines(keepends=False)))
    carts = []
    for jdx, line in enumerate(s.splitlines()):
        for idx, c in enumerate(line):
            if c in cart_dirs.keys():
                carts.append(MineCart(Loc2(idx, jdx), cart_dirs[c]))
    return MineTrack(tracks, carts)


def part_1(input_str: str):
    #input_str = test_input()
    track = parse_input(input_str)
    while not track.crashes:
        track.advance_carts()
    crash = track.crashes[0]
    return '{},{}'.format(crash.x, crash.y)


def part_2(input_str: str):
    # input_str = test_input()
    track = parse_input(input_str)
    while len(track.carts) > 1:
        track.advance_carts()
    cart = track.carts[0]
    return '{},{}'.format(cart.loc.x, cart.loc.y)


def test_input():
    test_num = 2
    if test_num == 0:
        return textwrap.dedent("""\
        |
        v
        |
        |
        ^
        |
        |""")
    elif test_num == 1:
        return textwrap.dedent("""\
        /->-\        
        |   |  /----\\
        | /-+--+-\  |
        | | |  | v  |
        \-+-/  \-+--/
          \------/   """)
    elif test_num == 2:
        return textwrap.dedent("""\
        />-<\  
        |   |  
        | /<+-\\
        | | | v
        \>+</ |
          |   ^
          \<->/""")


def main():
    input_str = get_input(13)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
