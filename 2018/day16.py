from getinput import get_input
import itertools
import textwrap
from util import grouper
import re


def all_opcodes():
    return [
        Program.addr,
        Program.addi,
        Program.mulr,
        Program.muli,
        Program.banr,
        Program.bani,
        Program.borr,
        Program.bori,
        Program.setr,
        Program.seti,
        Program.gtir,
        Program.gtri,
        Program.gtrr,
        Program.eqir,
        Program.eqri,
        Program.eqrr,
    ]


class Program(object):
    def __init__(self):
        self.reg = [0, 0, 0, 0]

    def addr(self, a, b, c):
        self.reg[c] = self.reg[a] + self.reg[b]

    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b

    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]

    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b

    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]

    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b

    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]

    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b

    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]

    def seti(self, a, b, c):
        self.reg[c] = a

    def gtir(self, a, b, c):
        self.reg[c] = 1 if a > self.reg[b] else 0

    def gtri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > b else 0

    def gtrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > self.reg[b] else 0

    def eqir(self, a, b, c):
        self.reg[c] = 1 if a == self.reg[b] else 0

    def eqri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == b else 0

    def eqrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == self.reg[b] else 0


def parse_input_1(s: str):
    effects = []
    for line1, line2, line3, _ in grouper(s.splitlines(keepends=False), 4):
        if not line1.startswith('Before'):
            break
        before = list(int(x) for x in re.findall(r'\[(.*)\]', line1)[0].split(','))
        instr = list(int(x) for x in line2.split())
        after = list(int(x) for x in re.findall(r'\[(.*)\]', line3)[0].split(','))
        effects.append((before, instr, after))
    return effects


def parse_input_2(s: str):
    return list(list(int(x) for x in line.split()) for line in s.splitlines(keepends=False)[3124:] if line)


def assign_opcodes(input_str: str):
    effects = parse_input_1(input_str)
    opcodes = dict()
    for idx in range(16):
        opcodes[idx] = all_opcodes()

    for before, instr, after in effects:
        num, a, b, c = instr
        new_opcodes = []
        for opcode in opcodes[num]:
            program = Program()
            program.reg = [x for x in before]
            opcode(program, a, b, c)
            if program.reg == after:
                new_opcodes.append(opcode)
        opcodes[num] = new_opcodes

    final_opcodes = dict()
    while len(final_opcodes) < 16:
        for k, v in opcodes.items():
            v = opcodes[k] = [x for x in v if x not in final_opcodes.values()]
            if k not in final_opcodes.keys() and not v:
                print(final_opcodes)
                raise RuntimeError('Can\'t assign opcodes.')
            if len(opcodes[k]) == 1:
                final_opcodes[k] = v[0]
    return final_opcodes


def part_1(input_str: str):
    effects = parse_input_1(input_str)
    num_with_3_plus = 0
    for before, instr, after in effects:
        a, b, c = instr[1:]
        num_opcodes = 0
        for opcode in all_opcodes():
            program = Program()
            program.reg = [x for x in before]
            opcode(program, a, b, c)
            if program.reg == after:
                num_opcodes += 1
        if num_opcodes >= 3:
            num_with_3_plus += 1
    return num_with_3_plus


def part_2(input_str: str):
    opcodes = assign_opcodes(input_str)
    instrs = parse_input_2(input_str)
    prog = Program()
    for opcode, a, b, c in instrs:
        opcodes[opcode](prog, a, b, c)
    return prog.reg[0]


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(16)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
