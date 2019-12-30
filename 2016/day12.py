from getinput import get_input


class Instruction(object):
    def __init__(self, s):
        words = s.split()
        self.t = words[0]
        self.params = words[1:]


class Computer(object):
    def __init__(self, instrs):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.cursor = 0
        self.instructions = instrs

    def execute(self):
        while 0 <= self.cursor < len(self.instructions):
            self.execute_next()

    def execute_next(self):
        instr = self.instructions[self.cursor]
        if instr.t == 'cpy':
            x, y = instr.params
            try:
                self.registers[y] = int(x)
            except ValueError:
                self.registers[y] = self.registers[x]
            self.cursor += 1
        elif instr.t == 'inc':
            x = instr.params[0]
            self.registers[x] += 1
            self.cursor += 1
        elif instr.t == 'dec':
            x = instr.params[0]
            self.registers[x] -= 1
            self.cursor += 1
        elif instr.t == 'jnz':
            x, y = instr.params
            try:
                if int(x) != 0:
                    self.cursor += int(y)
                else:
                    self.cursor += 1
            except ValueError:
                if self.registers[x] != 0:
                    self.cursor += int(y)
                else:
                    self.cursor += 1


def parse_input(s):
    instrs = []
    for line in s.splitlines(keepends=False):
        instrs.append(Instruction(line))
    return instrs


def part_1(big_str):
    instrs = parse_input(big_str)
    computer = Computer(instrs=instrs)
    computer.execute()
    return computer.registers['a']


def part_2(big_str):
    instrs = parse_input(big_str)
    computer = Computer(instrs=instrs)
    computer.registers['c'] = 1
    computer.execute()
    return computer.registers['a']


if __name__ == "__main__":
    the_big_str = get_input(12)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
