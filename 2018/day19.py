from getinput import get_input
import itertools
import textwrap
from program import Program, Decompile


def decompile_input(s: str):
    lines = s.splitlines(keepends=False)
    ip = int(lines[0][-1])
    print(lines)

    decompiler = Decompile(ip_register=ip)
    return '\n'.join(decompiler.decompile(idx, line) for idx, line in enumerate(lines[1:]))


def parse_input(s: str):
    return s


def part_1(input_str: str):
    # input_str = test_input()
    prog = Program()
    prog.init_from_str(input_str)
    prog.execute()
    return prog.reg[0]


def div_sum(n):
    return sum(x for x in range(1, n+1) if n % x == 0)


def part_2(input_str: str):
    # input_str = test_input()
    # print(decompile_input(input_str))
    return div_sum(10551389)


def test_input():
    return textwrap.dedent("""\
    #ip 0
    seti 5 0 1
    seti 6 0 2
    addi 0 1 0
    addr 1 2 3
    setr 1 0 0
    seti 8 0 4
    seti 9 0 5""")


def main():
    input_str = get_input(19)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
