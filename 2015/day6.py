from getinput import get_input
from enum import Enum
import itertools
import textwrap


class InstructionType(Enum):
    TURN_ON = 0
    TURN_OFF = 1
    TOGGLE = 2


class LightGrid(object):
    def __init__(self, width, height):
        self.grid = list([[0 for _ in range(width)] for _ in range(height)])

    def at(self, x, y):
        return self.grid[y][x]

    def turn_on(self, x, y):
        self.grid[y][x] = 1

    def turn_off(self, x, y):
        self.grid[y][x] = 0

    def toggle(self, x, y):
        self.grid[y][x] = (self.grid[y][x] + 1) % 2

    def num_lit(self):
        return sum(v for row in self.grid for v in row)


class BrightnessGrid(object):
    def __init__(self, width, height):
        self.grid = list([[0 for _ in range(width)] for _ in range(height)])

    def at(self, x, y):
        return self.grid[y][x]

    def turn_on(self, x, y):
        self.grid[y][x] += 1

    def turn_off(self, x, y):
        self.grid[y][x] = max(self.grid[y][x] - 1, 0)

    def toggle(self, x, y):
        self.grid[y][x] += 2

    def total_brightness(self):
        return sum(v for row in self.grid for v in row)


def parse_input(big_str):
    instrs = []
    for line in big_str.splitlines(keepends=False):
        args = line.split()
        if args[0] == 'turn' and args[1] == 'on':
            instr_type = InstructionType.TURN_ON
            ul_str = args[2]
            lr_str = args[4]
        elif args[0] == 'toggle':
            instr_type = InstructionType.TOGGLE
            ul_str = args[1]
            lr_str = args[3]
        elif args[0] == 'turn' and args[1] == 'off':
            instr_type = InstructionType.TURN_OFF
            ul_str = args[2]
            lr_str = args[4]
        else:
            raise RuntimeError('Can\'t parse input line <{}>'.format(line))

        ul = ul_str.split(',')
        lr = lr_str.split(',')
        instrs.append((instr_type, int(ul[0]), int(lr[0]), int(ul[1]), int(lr[1])))
    return instrs


def part_1(instrs):
    light_grid = LightGrid(1000, 1000)
    for instr_type, l, r, t, b in instrs:
        all_light_locs = itertools.product(range(l, r+1), range(t, b+1))
        if instr_type == InstructionType.TURN_ON:
            for x, y in all_light_locs:
                light_grid.turn_on(x, y)
        elif instr_type == InstructionType.TURN_OFF:
            for x, y in all_light_locs:
                light_grid.turn_off(x, y)
        elif instr_type == InstructionType.TOGGLE:
            for x, y in all_light_locs:
                light_grid.toggle(x, y)

    return light_grid.num_lit()


def part_2(instrs):
    light_grid = BrightnessGrid(1000, 1000)
    for instr_type, l, r, t, b in instrs:
        all_light_locs = itertools.product(range(l, r+1), range(t, b+1))
        if instr_type == InstructionType.TURN_ON:
            for x, y in all_light_locs:
                light_grid.turn_on(x, y)
        elif instr_type == InstructionType.TURN_OFF:
            for x, y in all_light_locs:
                light_grid.turn_off(x, y)
        elif instr_type == InstructionType.TOGGLE:
            for x, y in all_light_locs:
                light_grid.toggle(x, y)

    return light_grid.total_brightness()


if __name__ == "__main__":
    instructions = parse_input(get_input(day=6))

    print('Part 1:', part_1(instructions))
    print('Part 2:', part_2(instructions))
