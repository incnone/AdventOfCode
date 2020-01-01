from collections import defaultdict


class Program(object):
    def __init__(self, code):
        self.code = code
        self.registers = defaultdict(lambda: 0)
        self.sound = None
        self.cursor = 0
        self.linked_program = None
        self.received_values = []
        self.waiting = 0
        self.num_sent = 0

    def receive_value(self, x):
        self.received_values.append(x)

    def val(self, x):
        try:
            return int(x)
        except ValueError:
            return self.registers[x]

    def execute_next(self):
        cmd = self.code[self.cursor]
        words = cmd.split()
        opcode, params = words[0], words[1:]
        if opcode == 'snd':
            self.linked_program.receive_value(self.val(params[0]))
            self.cursor += 1
            self.num_sent += 1
        elif opcode == 'set':
            self.registers[params[0]] = self.val(params[1])
            self.cursor += 1
        elif opcode == 'add':
            self.registers[params[0]] += self.val(params[1])
            self.cursor += 1
        elif opcode == 'mul':
            self.registers[params[0]] *= self.val(params[1])
            self.cursor += 1
        elif opcode == 'mod':
            self.registers[params[0]] %= self.val(params[1])
            self.cursor += 1
        elif opcode == 'rcv':
            if self.received_values:
                self.registers[params[0]] = self.received_values.pop(0)
                self.waiting = 0
                self.cursor += 1
            else:
                self.waiting += 1
        elif opcode == 'jgz':
            if self.val(params[0]) > 0:
                self.cursor += self.val(params[1])
            else:
                self.cursor += 1

    def execute(self):
        while 0 <= self.cursor < len(self.code):
            self.execute_next()
