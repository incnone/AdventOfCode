from getinput import get_input
from grid import Loc2, Direction


class KeypadLoc(object):
    def __init__(self):
        self.loc = [0, 0]

    def move(self, ltr):
        if ltr == 'U':
            self.loc[1] = max(-1, self.loc[1] - 1)
        elif ltr == 'D':
            self.loc[1] = min(1, self.loc[1] + 1)
        elif ltr == 'L':
            self.loc[0] = max(-1, self.loc[0] - 1)
        elif ltr == 'R':
            self.loc[0] = min(1, self.loc[0] + 1)

    def digit(self):
        return str(3*(self.loc[1]+1) + self.loc[0]+2)


class HexKeypadLoc(object):
    def __init__(self):
        self.loc = [-2, 0]

    def move(self, ltr):
        old_loc = [self.loc[0], self.loc[1]]
        if ltr == 'U':
            self.loc[1] = self.loc[1] - 1
        elif ltr == 'D':
            self.loc[1] = self.loc[1] + 1
        elif ltr == 'L':
            self.loc[0] = self.loc[0] - 1
        elif ltr == 'R':
            self.loc[0] = self.loc[0] + 1
        if not self.valid():
            self.loc = old_loc

    def digit(self):
        digits = {
            (0, -2): '1',
            (-1, -1): '2',
            (0, -1): '3',
            (1, -1): '4',
            (-2, 0): '5',
            (-1, 0): '6',
            (0, 0): '7',
            (1, 0): '8',
            (2, 0): '9',
            (-1, 1): 'A',
            (0, 1): 'B',
            (1, 1): 'C',
            (0, 2): 'D'
        }
        return digits[tuple(self.loc)]

    def valid(self):
        return abs(self.loc[0]) + abs(self.loc[1]) <= 2


def part_1(dirs):
    keypad_loc = KeypadLoc()
    code = ''
    for dirline in dirs.splitlines(keepends=False):
        for c in dirline:
            keypad_loc.move(c)
        code += keypad_loc.digit()
    return code


def part_2(dirs):
    keypad_loc = HexKeypadLoc()
    code = ''
    for dirline in dirs.splitlines(keepends=False):
        for c in dirline:
            keypad_loc.move(c)
        code += keypad_loc.digit()
    return code

if __name__ == "__main__":
    the_dirs = get_input(2)

    print('Part 1:', part_1(the_dirs))
    print('Part 2:', part_2(the_dirs))
