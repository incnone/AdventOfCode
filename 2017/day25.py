from getinput import get_input
import itertools
import textwrap
from defaultlist import defaultlist


class TwoSidedTape(object):
    def __init__(self):
        self.right_tape = defaultlist(lambda: 0)    # includes 0
        self.left_tape = defaultlist(lambda: 0)     # starts at -1

    def __getitem__(self, item):
        if item >= 0:
            return self.right_tape[item]
        else:
            return self.left_tape[-item-1]

    def __setitem__(self, key, value):
        if key >= 0:
            self.right_tape[key] = value
        else:
            self.left_tape[-key-1] = value

    def __str__(self):
        return ''.join(str(x) for x in itertools.chain(reversed(self.left_tape), '|', self.right_tape))

    def __repr__(self):
        return ''.join(str(x) for x in itertools.chain(reversed(self.left_tape), '|', self.right_tape))

    def __iter__(self):
        return itertools.chain(reversed(self.left_tape), self.right_tape)


class TuringMachine(object):
    @staticmethod
    def parse_val(lines):
        write_val = int(lines[0].split()[-1].rstrip('.'))
        move_dir = 1 if lines[1].split()[-1].rstrip('.') == 'right' else -1
        next_state = lines[2].split()[-1].rstrip('.')
        return write_val, move_dir, next_state

    @staticmethod
    def parse_state(lines):
        return {
            lines[0].split()[-1].rstrip(':'): (TuringMachine.parse_val(lines[2:5]), TuringMachine.parse_val(lines[6:]))
        }

    @staticmethod
    def parse_input(s):
        lines = s.splitlines(keepends=False)
        starting_state = lines[0].split()[-1].rstrip('.')
        diagnostic_checksum_step = int(lines[1].split()[-2])
        states_dict = dict()

        cursor = 3
        while cursor < len(lines):
            states_dict.update(TuringMachine.parse_state(lines[cursor:cursor+9]))
            cursor += 10
        return starting_state, diagnostic_checksum_step, states_dict

    def __init__(self, s):
        self.state, self.checksum_at, self.code = TuringMachine.parse_input(s)
        self.cursor = 0
        self.tape = TwoSidedTape()

    def __str__(self):
        return ' '.join([str(self.cursor), self.state, str(self.tape)])

    def execute_next(self):
        instrs = self.code[self.state][self.tape[self.cursor]]
        self.tape[self.cursor] = instrs[0]
        self.cursor += instrs[1]
        self.state = instrs[2]

    def num_ones(self):
        return sum(self.tape)


def part_1(input_str):
    # input_str = test_input()
    machine = TuringMachine(input_str)

    for x in range(machine.checksum_at):
        machine.execute_next()

    return machine.num_ones()


def part_2(input_str):
    return


def test_input():
    return textwrap.dedent("""\
    Begin in state A.
    Perform a diagnostic checksum after 6 steps.
    
    In state A:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state B.
      If the current value is 1:
        - Write the value 0.
        - Move one slot to the left.
        - Continue with state B.
    
    In state B:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the left.
        - Continue with state A.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state A.""")


def main():
    input_str = get_input(25)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
