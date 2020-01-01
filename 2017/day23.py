from getinput import get_input
import itertools
from collections import defaultdict
from util import is_prime


class Program(object):
    def __init__(self, code):
        self.code = code
        self.registers = defaultdict(lambda: 0)
        self.cursor = 0
        self.mul_val = 0

    def val(self, x):
        try:
            return int(x)
        except ValueError:
            return self.registers[x]

    def execute_next(self):
        cmd = self.code[self.cursor]
        words = cmd.split()
        opcode, params = words[0], words[1:]
        if opcode == 'set':
            self.registers[params[0]] = self.val(params[1])
            self.cursor += 1
        elif opcode == 'sub':
            self.registers[params[0]] -= self.val(params[1])
            self.cursor += 1
        elif opcode == 'mul':
            self.registers[params[0]] *= self.val(params[1])
            self.cursor += 1
            self.mul_val += 1
        elif opcode == 'jnz':
            if self.val(params[0]) != 0:
                self.cursor += self.val(params[1])
            else:
                self.cursor += 1

    def execute(self):
        while 0 <= self.cursor < len(self.code):
            self.execute_next()


def parse_input(s):
    return s.splitlines(keepends=False)


def part_1(input_str):
    prog = Program(parse_input(input_str))
    prog.execute()
    return prog.mul_val


def part_2(input_str):
    h = 0
    for b in range(108100, 108100+17000+17, 17):
        if not is_prime(b):
            h += 1
    return h


def main():
    input_str = get_input(23)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
