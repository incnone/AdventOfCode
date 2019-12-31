from getinput import get_input
import itertools
from computer import Instruction, Computer


def parse_input(s):
    computer = Computer()
    for line in s.splitlines(keepends=False):
        computer.instructions.append(Instruction(line))
    return computer


def part_1(input_str):
    computer = parse_input(input_str)
    computer.execute()
    return max(computer.registers.values())


def part_2(input_str):
    computer = parse_input(input_str)
    computer.execute()
    return computer.max_register_val


def main():
    input_str = get_input(8)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
