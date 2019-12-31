from collections import defaultdict
import operator
from typing import List


class Instruction(object):
    ops_table = {
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
        '==': operator.eq,
        '!=': operator.ne
    }

    def __init__(self, s):
        words = s.split()
        self.register = words[0]
        self.increment = int(words[2]) * (1 if words[1] == 'inc' else -1)
        self.conditional_register = words[4]
        self.condition_op = Instruction.ops_table[words[5]]
        self.condition_value = int(words[6])


class Computer(object):
    def __init__(self):
        self.instructions = []                      # type: List[Instruction]
        self.registers = defaultdict(lambda: 0)
        self.cursor = 0
        self.max_register_val = -99999999

    def execute_current(self):
        instr = self.instructions[self.cursor]
        if instr.condition_op(self.registers[instr.conditional_register], instr.condition_value):
            self.registers[instr.register] += instr.increment
            self.max_register_val = max(self.max_register_val, self.registers[instr.register])

    def execute(self):
        while self.cursor < len(self.instructions):
            self.execute_current()
            self.cursor += 1
