import textwrap


class CathCPU(object):
    def __init__(self, program):
        self.cycles = 0
        self.x = 1
        self.program = program
        self._cursor = 0
        self._val_to_add = None

    def cycle(self):
        if self._val_to_add is not None:
            self.x += self._val_to_add
            self._val_to_add = None
            self._cursor += 1
        else:
            cmd = self.program[self._cursor].split()
            if cmd[0] == 'noop':
                self._cursor += 1
            elif cmd[0] == 'addx':
                self._val_to_add = int(cmd[1])

        self.cycles += 1

    def good(self):
        return 0 <= self._cursor < len(self.program)


def get_test_input() -> str:
    return textwrap.dedent("""\
    addx 15
    addx -11
    addx 6
    addx -3
    addx 5
    addx -1
    addx -8
    addx 13
    addx 4
    noop
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx -35
    addx 1
    addx 24
    addx -19
    addx 1
    addx 16
    addx -11
    noop
    noop
    addx 21
    addx -15
    noop
    noop
    addx -3
    addx 9
    addx 1
    addx -3
    addx 8
    addx 1
    addx 5
    noop
    noop
    noop
    noop
    noop
    addx -36
    noop
    addx 1
    addx 7
    noop
    noop
    noop
    addx 2
    addx 6
    noop
    noop
    noop
    noop
    noop
    addx 1
    noop
    noop
    addx 7
    addx 1
    noop
    addx -13
    addx 13
    addx 7
    noop
    addx 1
    addx -33
    noop
    noop
    noop
    addx 2
    noop
    noop
    noop
    addx 8
    noop
    addx -1
    addx 2
    addx 1
    noop
    addx 17
    addx -9
    addx 1
    addx 1
    addx -3
    addx 11
    noop
    noop
    addx 1
    noop
    addx 1
    noop
    noop
    addx -13
    addx -19
    addx 1
    addx 3
    addx 26
    addx -30
    addx 12
    addx -1
    addx 3
    addx 1
    noop
    noop
    noop
    addx -9
    addx 18
    addx 1
    addx 2
    noop
    noop
    addx 9
    noop
    noop
    noop
    addx -1
    addx 2
    addx -37
    addx 1
    addx 3
    noop
    addx 15
    addx -21
    addx 22
    addx -6
    addx 1
    noop
    addx 2
    addx 1
    noop
    addx -10
    noop
    noop
    addx 20
    addx 1
    addx 2
    addx 2
    addx -6
    addx -11
    noop
    noop
    noop""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return data


def part_1(data):
    cpu = CathCPU(program=data)
    signal_strength = 0
    while cpu.good():
        cpu.cycle()
        if cpu.cycles % 40 == 19:
            signal_strength += cpu.x * (cpu.cycles + 1)

    print(f'Part 1: {signal_strength}')


def part_2(data):
    cpu = CathCPU(program=data)

    output = ''
    while cpu.good():
        x = cpu.cycles % 40
        output += '#' if -1 <= x - cpu.x <= 1 else ' '
        if x == 39:
            output += '\n'
        cpu.cycle()

    print(f'Part 2: \n{output}')


def main():
    data = read_input(day_number=10, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
