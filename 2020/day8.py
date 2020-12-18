import textwrap
from typing import List
import copy


class Instruction(object):
    def __init__(self, s: str):
        words = s.strip().split()
        self.type = words[0]
        self.val = int(words[1])

    def __copy__(self, other):
        self.type = other.type
        self.val = other.val


class Program(object):
    def __init__(self, code: List[Instruction]):
        self.instrs = code
        self.accum = 0
        self.cursor = 0

    def loops(self):
        already_ran = set()
        while self.cursor not in already_ran:
            already_ran.add(self.cursor)
            self.step()
            if self.cursor == len(self.instrs):
                return False
        return True

    def execute_until_loop(self):
        already_ran = set()
        while self.cursor not in already_ran:
            already_ran.add(self.cursor)
            self.step()

    def step(self):
        current = self.instrs[self.cursor]
        if current.type == 'acc':
            self.accum += current.val
            self.cursor += 1
        elif current.type == 'jmp':
            self.cursor += current.val
        elif current.type == 'nop':
            self.cursor += 1


def get_test_input() -> str:
    return textwrap.dedent("""\
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(Instruction(line))
    return data


def part_1(data):
    prog = Program(data)
    prog.execute_until_loop()
    print('Part 1:', prog.accum)


def part_2(data):
    for idx in range(len(data)):
        data_copy = copy.deepcopy(data)
        if data_copy[idx].type == 'acc':
            continue
        elif data_copy[idx].type == 'jmp':
            data_copy[idx].type = 'nop'
        elif data_copy[idx].type == 'nop':
            data_copy[idx].type = 'jmp'
        prog = Program(data_copy)
        if not prog.loops():
            print('Part 2:', prog.accum)
            return


def main():
    data = read_input(day_number=8, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
