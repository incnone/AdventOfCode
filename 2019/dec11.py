from enum import Enum
from collections import defaultdict
from defaultlist import defaultlist
from typing import Dict, Tuple


class InstructionType(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class IntcodeProgram(object):
    num_params = {
        InstructionType.ADD: 3,
        InstructionType.MULTIPLY: 3,
        InstructionType.INPUT: 1,
        InstructionType.OUTPUT: 1,
        InstructionType.JUMP_IF_TRUE: 2,
        InstructionType.JUMP_IF_FALSE: 2,
        InstructionType.LESS_THAN: 3,
        InstructionType.EQUALS: 3,
        InstructionType.ADJUST_RELATIVE_BASE: 1,
        InstructionType.HALT: 0,
    }

    def __init__(self, code: str):
        self.code = defaultlist(lambda: 0)
        for s in code.split(','):
            self.code.append(int(s))
        # self.code = [int(s) for s in code.split(',')]
        self.cursor = 0
        self.relative_base = 0
        self.halt = False
        self.input = []
        self.output = []

    def read_input(self, value):
        self.input.append(value)

    def read_inputs(self, values):
        self.input += values

    def read_output(self):
        return self.output.pop(0)

    def execute_next(self):
        FULL_DEBUG = False

        opcode = self.code[self.cursor]
        if FULL_DEBUG:
            print("{}: {} (relbase {})".format(self.cursor, opcode, self.relative_base))

        instruction = InstructionType(int(str(opcode)[-2:]))
        num_p = self.num_params[instruction]
        parameter_modes = [ParameterMode.POSITION]*num_p
        for idx, char in enumerate(reversed(str(opcode)[:-2])):
            parameter_modes[idx] = ParameterMode(int(char))
        values = self.values(parameter_modes)
        addresses = self.addresses(parameter_modes)

        if FULL_DEBUG:
            print(instruction.name, parameter_modes, values, addresses)

        increment_cursor = True
        if instruction == InstructionType.ADD:
            self.code[addresses[2]] = values[0] + values[1]
        elif instruction == InstructionType.MULTIPLY:
            self.code[addresses[2]] = values[0] * values[1]
        elif instruction == InstructionType.INPUT:
            self.code[addresses[0]] = self.input.pop(0)
        elif instruction == InstructionType.OUTPUT:
            self.output.append(values[0])
        elif instruction == InstructionType.JUMP_IF_TRUE:
            if values[0]:
                self.cursor = values[1]
                increment_cursor = False
        elif instruction == InstructionType.JUMP_IF_FALSE:
            if not values[0]:
                self.cursor = values[1]
                increment_cursor = False
        elif instruction == InstructionType.LESS_THAN:
            self.code[addresses[2]] = 1 if values[0] < values[1] else 0
        elif instruction == InstructionType.EQUALS:
            self.code[addresses[2]] = 1 if values[0] == values[1] else 0
        elif instruction == InstructionType.ADJUST_RELATIVE_BASE:
            self.relative_base += values[0]
        elif instruction == InstructionType.HALT:
            self.halt = True

        if increment_cursor:
            self.cursor += num_p + 1

        if FULL_DEBUG:
            print(self.code)

    def execute(self):
        while not self.halt:
            self.execute_next()

    def execute_until_output(self):
        while not self.output and not self.halt:
            self.execute_next()

    def values(self, parameter_modes):
        return [
            self.code[self.cursor+jdx+1] if parameter_modes[jdx] == ParameterMode.IMMEDIATE
            else self.code[self.relative_base+self.code[self.cursor+jdx+1]] if parameter_modes[jdx] == ParameterMode.RELATIVE
            else self.code[self.code[self.cursor+jdx+1]]   # if parameter_modes[jdx] == ParameterMode.POSITION
            for jdx in range(len(parameter_modes))
        ]

    def addresses(self, parameter_modes):
        return [
            self.relative_base + self.code[self.cursor+jdx+1] if parameter_modes[jdx] == ParameterMode.RELATIVE
            else self.code[self.cursor+jdx+1]
            for jdx in range(len(parameter_modes))
        ]

    def params(self, parameter_modes):
        return [self.code[self.cursor+jdx+1] for jdx in range(len(parameter_modes))]


class HullColor(Enum):
    BLACK = 0
    WHITE = 1

    def colorstr(self):
        if self == HullColor.BLACK:
            return ' '
        else:
            return '#'


class HullPanel(object):
    def __init__(self, default_color: HullColor):
        self.default_color = default_color
        self.colored_panels = defaultdict(lambda: self.default_color)    # type: Dict[Tuple[int, int], HullColor]

    def paint(self, loc, color):
        self.colored_panels[loc] = color

    def color(self, loc):
        return self.colored_panels[loc]

    def get_str(self):
        # Inefficient but meh
        min_x = min([p[0] for p in self.colored_panels.keys()])
        max_x = max([p[0] for p in self.colored_panels.keys()])
        min_y = min([p[1] for p in self.colored_panels.keys()])
        max_y = max([p[1] for p in self.colored_panels.keys()])

        ret = ''
        for row in range(max_x, min_x - 1, -1):
            rowstr = ''.join([self.colored_panels[(row, col)].colorstr() for col in range(max_y, min_y-1, -1)])
            ret += rowstr + '\n'
        return ret


class HullRobot(object):
    def __init__(self, loc: Tuple[int, int], hull_panel: HullPanel, program: IntcodeProgram):
        self.loc = loc      # type: Tuple[int, int]
        self.dir = (1, 0)
        self.hull_panel = hull_panel
        self.program = program
        self.painted_tiles = set()
        self.num_steps = 0

    def move_forward(self):
        self.loc = (self.loc[0] + self.dir[0], self.loc[1] + self.dir[1])

    def turn_right(self):
        self.dir = (self.dir[1], -self.dir[0])

    def turn_left(self):
        self.dir = (-self.dir[1], self.dir[0])

    def turn_code(self, code):
        if code == 0:
            self.turn_left()
        elif code == 1:
            self.turn_right()
        else:
            raise RuntimeError('Incorrect turn code ({})'.format(code))

    def paint(self, color: HullColor):
        self.hull_panel.paint(self.loc, color)

    @property
    def color(self) -> HullColor:
        return self.hull_panel.color(self.loc)

    def execute_step(self):
        self.program.read_input(self.color.value)
        self.program.execute_until_output()
        if self.program.halt:
            return
        self.paint(HullColor(self.program.read_output()))
        self.painted_tiles.add(self.loc)
        self.program.execute_until_output()
        if self.program.halt:
            return
        self.turn_code(self.program.read_output())
        self.move_forward()
        self.num_steps += 1

    def execute(self):
        while not self.program.halt:
            self.execute_step()


if __name__ == "__main__":
    with open('input/dec11.txt', 'r') as file:
        program_code = file.readline()

    program = IntcodeProgram(program_code)
    hull_panel = HullPanel(HullColor.BLACK)
    hull_panel.paint((0, 0), HullColor.WHITE)   # Emergency Robot Starting Panel
    robot = HullRobot(loc=(0, 0), hull_panel=hull_panel, program=program)

    robot.execute()
    print(robot.hull_panel.get_str())
