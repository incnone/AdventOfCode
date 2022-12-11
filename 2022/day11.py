import textwrap
import re
import math
from typing import Dict


def get_test_input() -> str:
    return textwrap.dedent("""\
    Monkey 0:
      Starting items: 79, 98
      Operation: new = old * 19
      Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3
    
    Monkey 1:
      Starting items: 54, 65, 75, 74
      Operation: new = old + 6
      Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0
    
    Monkey 2:
      Starting items: 79, 60, 97
      Operation: new = old * old
      Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3
    
    Monkey 3:
      Starting items: 74
      Operation: new = old + 3
      Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


class Monkey(object):
    monkey_format = re.compile(r'Monkey (\d+):\n'
                               r'\s*Starting items: ([,\d ]*)\n'
                               r'\s*Operation: new = ([^\n]*)\n'
                               r'\s*Test: divisible by (\d+)\n'
                               r'\s*If true: throw to monkey (\d+)\n'
                               r'\s*If false: throw to monkey (\d+)')

    def __init__(self, s):
        m = Monkey.monkey_format.match(s)
        if m is None:
            raise RuntimeError(f'Invalid Monkey initialization string: {s}')

        self.index = int(m.group(1))
        self.items = list(int(x) for x in m.group(2).split(','))
        self.operation_text = m.group(3)
        self.operation = self.parse_optext(self.operation_text)
        self.test_divby = int(m.group(4))
        self.iftrue_monkey = int(m.group(5))
        self.iffalse_monkey = int(m.group(6))
        self.num_inspections = 0

    def __str__(self):
        return textwrap.dedent(f"""\
        Monkey {self.index}:
          Items: {','.join(str(x) for x in self.items)}
          Operation: new = {self.operation_text}
          Test: divisible by {self.test_divby}
            If true: throw to monkey {self.iftrue_monkey}
            If false: throw to monkey {self.iffalse_monkey}""")

    def __repr__(self):
        return f"M({self.index}, {self.items}, {self.operation_text}, " \
               f"{self.test_divby}, {self.iftrue_monkey}, {self.iffalse_monkey})"

    def take_turn(self, monkeys, lcm, do_divbythree):
        for item in self.items:
            new_worry = self.operation(item)
            if do_divbythree:
                new_worry = new_worry // 3
            new_worry = new_worry % lcm

            if new_worry % self.test_divby == 0:
                monkeys[self.iftrue_monkey].items.append(new_worry)
            else:
                monkeys[self.iffalse_monkey].items.append(new_worry)
        self.num_inspections += len(self.items)
        self.items = []

    @staticmethod
    def parse_optext(optext):
        args = optext.split()
        assert args[0] == 'old'
        if args[1] == '+':
            if args[2] == 'old':
                return lambda x: x + x
            else:
                return lambda x: x + int(args[2])
        elif args[1] == '*':
            if args[2] == 'old':
                return lambda x: x * x
            else:
                return lambda x: x * int(args[2])
        else:
            raise RuntimeError(f'Didn\'t recognize optext {optext}')


def parse_input(s: str):
    data = dict()
    for mstr in s.split('\n\n'):
        monkey = Monkey(mstr)
        data[monkey.index] = monkey
    return data


def get_monkey_lcm(monkeys):
    return math.lcm(*[m.test_divby for m in monkeys.values()])


def part_1(monkeys):
    lcm = get_monkey_lcm(monkeys)

    num_rounds = 20
    num_monkeys = len(monkeys.keys())
    for r in range(num_rounds):
        for mdx in range(num_monkeys):
            monkeys[mdx].take_turn(monkeys, lcm, True)
        # print(f'After round {r+1}:')
        # for mdx, monkey in monkeys.items():
        #     print(f'  Monkey {mdx}: {monkey.items}')
        # print('\n')

    for mdx, monkey in monkeys.items():
        print(f'Monkey {mdx} inspected items {monkey.num_inspections} times.')

    inspects = sorted([m.num_inspections for m in monkeys.values()], reverse=True)
    print(f'Part 1: {inspects[0]*inspects[1]}')


def part_2(monkeys):
    lcm = get_monkey_lcm(monkeys)
    print(lcm)

    num_rounds = 10000
    num_monkeys = len(monkeys.keys())
    for r in range(num_rounds):
        for mdx in range(num_monkeys):
            monkeys[mdx].take_turn(monkeys, lcm, False)

        # if r+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
        #     print(f'== After round {r+1} ==')
        #     for mdx, monkey in monkeys.items():
        #         print(f'  Monkey {mdx} inspected items {monkey.num_inspections} times.')
        #     print('\n')

    # for mdx, monkey in monkeys.items():
    #     print(f'Monkey {mdx} inspected items {monkey.num_inspections} times.')

    inspects = sorted([m.num_inspections for m in monkeys.values()], reverse=True)
    print(f'Part 2: {inspects[0]*inspects[1]}')


def main():
    data = read_input(day_number=11, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
