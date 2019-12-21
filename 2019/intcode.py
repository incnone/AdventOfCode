from enum import Enum
from defaultlist import defaultlist


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


class ListOutput(object):
    """Reads outputs from an IntcodeProgram and stores them in a list."""
    def __init__(self):
        self.output_list = []

    def read_output(self, value):
        self.output_list.append(value)


class ListInput(object):
    """Provides a list of inputs to an IntcodeProgram"""
    def __init__(self, input_list=None):
        self.input_list = input_list if input_list is not None else []
        self.cursor = 0

    def get_input(self):
        try:
            return self.input_list[self.cursor]
        finally:
            self.cursor += 1


class StringInput(object):
    """Reads inputs to an IntcodeProgram from a string, converting to ascii values."""
    def __init__(self):
        self.input_str = None
        self.cursor = 0

    def get_input(self):
        try:
            return ord(self.input_str[self.cursor])
        finally:
            self.cursor += 1


class ConsoleInput(object):
    """Provides input to an IntcodeProgram through stdin, using ascii conversion if desired"""
    def __init__(self, use_ascii=True):
        self.use_ascii = use_ascii
        self.buffer = []

    def get_input(self):
        if not self.buffer:
            raw_input = input()
            for x in raw_input:
                self.buffer.append(ord(x) if self.use_ascii else x)
            if self.use_ascii:
                self.buffer.append(ord('\n'))

        return self.buffer.pop(0)


class ConsoleOutput(object):
    """Provides stdout output for an IntcodeProgram, using ascii conversion if desired"""
    def __init__(self, use_ascii=True):
        self.use_ascii = use_ascii

    def read_output(self, value):
        if self.use_ascii and value > 255:  # Hack
            print('<Non-ascii: {}>'.format(value), end="")
        else:
            try:
                print(chr(value) if self.use_ascii else value, end="")
            except TypeError:
                print(value, end="")


class IOHandlerL2L(ListInput, ListOutput):
    def __init__(self, input_list=None):
        ListInput.__init__(self, input_list=input_list)
        ListOutput.__init__(self)


class IOHandlerC2C(ConsoleInput, ConsoleOutput):
    def __init__(self, use_ascii=True):
        ConsoleInput.__init__(self, use_ascii=use_ascii)
        ConsoleOutput.__init__(self, use_ascii=use_ascii)


class IOHandlerC2L(ConsoleInput, ListOutput):
    def __init__(self, use_ascii=True):
        ConsoleInput.__init__(self, use_ascii=use_ascii)
        ListOutput.__init__(self)


class IOHandlerL2C(ListInput, ConsoleOutput):
    def __init__(self, input_list=None, use_ascii=True):
        ListInput.__init__(self, input_list=input_list)
        ConsoleOutput.__init__(self, use_ascii=use_ascii)


class IOHandlerS2C(StringInput, ConsoleOutput):
    def __init__(self):
        StringInput.__init__(self)
        ConsoleOutput.__init__(self, use_ascii=True)


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

    @staticmethod
    def console_program(code: str, use_ascii=True):
        return IntcodeProgram(code=code, io_handler=IOHandlerC2C(use_ascii=use_ascii))

    @staticmethod
    def list_program(code: str, input_list=None):
        return IntcodeProgram(code=code, io_handler=IOHandlerL2L(input_list=input_list))

    def __init__(self, code: str, io_handler):
        self.code = defaultlist(lambda: 0)
        for s in code.split(','):
            self.code.append(int(s))
        # self.code = [int(s) for s in code.split(',')]
        self.cursor = 0
        self.relative_base = 0
        self.halt = False
        self.io_handler = io_handler

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
            self.code[addresses[0]] = self.io_handler.get_input()
        elif instruction == InstructionType.OUTPUT:
            self.io_handler.read_output(values[0])
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


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZ_PADDLE = 3
    BALL = 4

    def get_char(self):
        if self == TileType.EMPTY:
            return ' '
        elif self == TileType.WALL:
            return '#'
        elif self == TileType.BLOCK:
            return 'X'
        elif self == TileType.HORIZ_PADDLE:
            return '-'
        elif self == TileType.BALL:
            return 'o'


class BlockGame(object):
    def __init__(self):
        self.tiles = dict()
        self.score = 0
        self.paddle_x = None
        self.ball_x = None

    def interpret(self, x):
        if x[0] == -1 and x[1] == 0:
            self.score = x[2]
            return

        tile_type = TileType(x[2])
        self.tiles[(x[0], x[1])] = tile_type
        if tile_type == TileType.HORIZ_PADDLE:
            self.paddle_x = x[0]
        elif tile_type == TileType.BALL:
            self.ball_x = x[0]

    def get_input(self):
        if self.paddle_x is None or self.ball_x is None:
            return 0
        elif self.paddle_x > self.ball_x:
            return -1
        elif self.paddle_x < self.ball_x:
            return 1
        else:
            return 0

    def get_picture(self):
        min_x = min([x[0] for x in self.tiles.keys()])
        max_x = max([x[0] for x in self.tiles.keys()])
        min_y = min([x[1] for x in self.tiles.keys()])
        max_y = max([x[1] for x in self.tiles.keys()])

        ret = ''
        for y in range(min_y, max_y+1, 1):
            for x in range(min_x, max_x + 1, 1):
                if (x, y) in self.tiles:
                    ret += self.tiles[(x, y)].get_char()
                else:
                    ret += ' '
            ret += '\n'

        ret += '\n'
        ret += "Score: {}\n".format(self.score)
        return ret
