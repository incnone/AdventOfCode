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


def test_1():
    code = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    prog = IntcodeProgram(code)
    prog.execute()
    return 'Passed' if prog.output == [int(s) for s in code.split(',')] else 'Failed'


def test_2():
    code = "1102,34915192,34915192,7,4,7,99,0"
    prog = IntcodeProgram(code)
    prog.execute()
    return 'Passed' if len(str(prog.output[0])) == 16 else 'Failed'


def test_3():
    code = "104,1125899906842624,99"
    prog = IntcodeProgram(code)
    prog.execute()
    return 'Passed' if prog.output[0] == 1125899906842624 else 'Failed'


if __name__ == "__main__":
    # print("Test 1:", test_1())
    # print("Test 2:", test_2())
    # print("Test 3:", test_3())

    with open('input/dec9.txt', 'r') as file:
        program_code = file.readline()

    program = IntcodeProgram(program_code)
    program.read_input(2)
    program.execute()
    print(program.output)
