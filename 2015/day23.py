from getinput import get_input
from enum import Enum
import itertools


class Computer(object):
    def __init__(self, instrs):
        self.instrs = instrs
        self.registers = [0, 0]
        self.cursor = 0

    @staticmethod
    def get_register(s):
        if s == 'a':
            return 0
        elif s == 'b':
            return 1

    def execute(self):
        while True:
            try:
                self.execute_one()
            except IndexError:
                break

    def execute_one(self):
        old_cursor = self.cursor
        parsed = self.instrs[self.cursor].split()
        if parsed[0] == 'hlf':
            reg = self.get_register(parsed[1])
            self.registers[reg] = self.registers[reg] // 2
            self.cursor += 1
        elif parsed[0] == 'tpl':
            reg = self.get_register(parsed[1])
            self.registers[reg] = self.registers[reg] * 3
            self.cursor += 1
        elif parsed[0] == 'inc':
            reg = self.get_register(parsed[1])
            self.registers[reg] = self.registers[reg] + 1
            self.cursor += 1
        elif parsed[0] == 'jmp':
            self.cursor += int(parsed[1])
        elif parsed[0] == 'jie':
            val = self.registers[self.get_register(parsed[1][:1])]
            if val % 2 == 0:
                self.cursor += int(parsed[2])
            else:
                self.cursor += 1
        elif parsed[0] == 'jio':
            val = self.registers[self.get_register(parsed[1][:1])]
            if val == 1:
                self.cursor += int(parsed[2])
            else:
                self.cursor += 1
        print(old_cursor+1, self.registers)


def parse_input(s):
    instrs = []
    for line in s.splitlines(keepends=False):
        instrs.append(line)
    return instrs


def part_1(instrs):
    program = Computer(instrs=instrs)
    program.execute()
    return program.registers[1]


def part_2(instrs):
    program = Computer(instrs=instrs)
    program.registers[0] = 1
    program.execute()
    return program.registers[1]


if __name__ == "__main__":
    the_instrs = parse_input(get_input(23))

    print('Part 1:', part_1(the_instrs))
    print('Part 2:', part_2(the_instrs))
