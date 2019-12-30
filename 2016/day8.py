from getinput import get_input
from enum import Enum
import itertools
import textwrap


class InstructionType(Enum):
    RECT = 0
    ROTATE_COLUMN = 1
    ROTATE_ROW = 2


class Instruction(object):
    @staticmethod
    def from_str(s):
        words = s.split()
        if words[0] == 'rect':
            t = InstructionType.RECT
            coords = words[1].split('x')
            params = (int(coords[0]), int(coords[1]))
        elif words[0] == 'rotate':
            if words[1] == 'row':
                t = InstructionType.ROTATE_ROW
            elif words[1] == 'column':
                t = InstructionType.ROTATE_COLUMN
            else:
                raise RuntimeError('Bad string {}'.format(s))
            row = int((words[2].split('='))[1])
            amt = int(words[-1])
            params = (row, amt)
        else:
            raise RuntimeError('Bad string {}'.format(s))

        return Instruction(t, *params)

    def __init__(self, t, *args):
        self.t = t
        self.params = args


class LightGrid(object):
    _neighbor_pairs = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]

    def __init__(self, width, height):
        self.grid = list([[0 for _ in range(width)] for _ in range(height)])
        self.width = width
        self.height = height

    def __str__(self):
        return '\n'.join(''.join('#' if v else '.' for v in row) for row in self.grid)

    def at(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError
        return self.grid[y][x]

    def turn_on(self, x, y):
        self.grid[y][x] = 1

    def turn_off(self, x, y):
        self.grid[y][x] = 0

    def toggle(self, x, y):
        self.grid[y][x] = (self.grid[y][x] + 1) % 2

    def execute(self, instr):
        if instr.t == InstructionType.RECT:
            for x, y in itertools.product(range(instr.params[0]), range(instr.params[1])):
                self.turn_on(x, y)
        elif instr.t == InstructionType.ROTATE_ROW:
            y, r = instr.params
            row = list([v for v in self.grid[y]])
            for i in range(self.width):
                self.grid[y][i] = row[(i - r) % self.width]
        elif instr.t == InstructionType.ROTATE_COLUMN:
            x, r = instr.params
            col = list([self.grid[j][x] for j in range(self.height)])
            for j in range(self.height):
                self.grid[j][x] = col[(j - r) % self.height]

    def num_lit(self):
        return sum(v for row in self.grid for v in row)

    def num_lit_neighbors(self, x, y):
        num_lit = 0
        for offset in LightGrid._neighbor_pairs:
            try:
                num_lit += self.at(x+offset[0], y+offset[1])
            except IndexError:
                pass
        return num_lit


def parse_input(big_str):
    instrs = []
    for line in big_str.splitlines(keepends=False):
        instrs.append(Instruction.from_str(line))
    return instrs


def part_1(big_str):
    instrs = parse_input(big_str)
    light_grid = LightGrid(width=50, height=6)
    for instr in instrs:
        light_grid.execute(instr)
    return light_grid.num_lit()


def part_2(big_str):
    instrs = parse_input(big_str)
    light_grid = LightGrid(width=50, height=6)
    for instr in instrs:
        light_grid.execute(instr)
    return '\n' + str(light_grid)


def test_str():
    return textwrap.dedent("""\
    rect 3x2
    rotate column x=1 by 1
    rotate row y=0 by 4
    rotate column x=1 by 1""")


if __name__ == "__main__":
    the_big_str = get_input(8)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
