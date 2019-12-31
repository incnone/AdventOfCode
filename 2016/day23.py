from getinput import get_input
import textwrap
import math


class Instruction(object):
    def __init__(self, s):
        words = s.split()
        self.t = words[0]
        self.params = words[1:]

    def toggle(self):
        toggle_dict = {
            'inc': 'dec',
            'dec': 'inc',
            'tgl': 'inc',
            'cpy': 'jnz',
            'jnz': 'cpy'
        }
        self.t = toggle_dict[self.t]


class Computer(object):
    def __init__(self, instrs):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.cursor = 0
        self.instructions = instrs

    def to_rval(self, x):
        return self.registers[x] if x in self.registers else int(x)

    def execute(self):
        while 0 <= self.cursor < len(self.instructions):
            if self.cursor == 10:
                print(self.registers)
            self.execute_next()

    def execute_next(self):
        instr = self.instructions[self.cursor]

        if instr.t == 'cpy':
            x, y = instr.params
            if y not in self.registers.keys():
                return
            self.registers[y] = self.to_rval(x)
            self.cursor += 1

        elif instr.t == 'inc':
            x = instr.params[0]
            if x not in self.registers.keys():
                return
            self.registers[x] += 1
            self.cursor += 1

        elif instr.t == 'dec':
            x = instr.params[0]
            if x not in self.registers.keys():
                return
            self.registers[x] -= 1
            self.cursor += 1

        elif instr.t == 'jnz':
            x, y = tuple(self.to_rval(k) for k in instr.params)
            if x != 0:
                self.cursor += y
            else:
                self.cursor += 1

        elif instr.t == 'tgl':
            idx = self.cursor + self.to_rval(instr.params[0])
            if 0 <= idx < len(self.instructions):
                self.instructions[idx].toggle()
            self.cursor += 1

        elif instr.t == 'add':
            x, y, z = instr.params
            x, y = (self.to_rval(x), self.to_rval(y))
            self.registers[z] = x+y

        elif instr.t == 'mul':
            x, y, z = instr.params
            x, y = (self.to_rval(x), self.to_rval(y))
            self.registers[z] = x*y


def parse_input(s):
    instrs = []
    for line in s.splitlines(keepends=False):
        instrs.append(Instruction(line))
    return instrs


def test_input():
    return textwrap.dedent("""\
    cpy 2 a
    tgl a
    tgl a
    tgl a
    cpy 1 a
    dec a
    dec a""")


def part_1(big_str):
    computer = Computer(instrs=parse_input(big_str))
    computer.registers['a'] = 7
    computer.execute()
    return computer.registers['a']


def part_2():
    # Careful inspection of my input code shows that it computes (x! + 95*91) when x >= 6
    return math.factorial(12) + 95*91


if __name__ == "__main__":
    the_big_str = get_input(23)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2())
