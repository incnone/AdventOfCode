from enum import Enum
from typing import List


class InstructionType(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


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
        InstructionType.HALT: 0,
    }

    def __init__(self, code: str, input: List[int]):
        self.code = [int(s) for s in code.split(',')]
        self.cursor = 0
        self.halt = False
        self.input = input
        self.output = []

    def execute_next(self):
        opcode = self.code[self.cursor]
        # print("{}: {}".format(self.cursor, opcode))
        instruction = InstructionType(int(str(opcode)[-2:]))
        num_p = self.num_params[instruction]
        parameter_modes = [ParameterMode.POSITION]*num_p
        for idx, char in enumerate(reversed(str(opcode)[:-2])):
            parameter_modes[idx] = ParameterMode(int(char))
        values = self.values(parameter_modes)
        addresses = self.params(parameter_modes)
        # print(instruction.name, parameter_modes, values)

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
        elif instruction == InstructionType.HALT:
            self.halt = True

        if increment_cursor:
            self.cursor += num_p + 1

    def execute(self):
        while not self.halt:
            self.execute_next()

    def values(self, parameter_modes):
        return [self.code[self.cursor+jdx+1]
                if parameter_modes[jdx] == ParameterMode.IMMEDIATE
                else self.code[self.code[self.cursor+jdx+1]]
                for jdx in range(len(parameter_modes))]

    def params(self, parameter_modes):
        return [self.code[self.cursor+jdx+1] for jdx in range(len(parameter_modes))]


if __name__ == "__main__":
    with open('input/dec5.txt', 'r') as file:
        prog = IntcodeProgram(file.readline(), [5])

    prog.execute()
    print(prog.output)
