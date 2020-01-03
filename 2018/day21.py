from getinput import get_input
import itertools
import textwrap
from program import Program, Decompile


def decompile_input(s: str):
    lines = s.splitlines(keepends=False)
    ip = int(lines[0][-1])

    decompiler = Decompile(ip_register=ip)
    return '\n'.join(decompiler.decompile(idx, line) for idx, line in enumerate(lines[1:]))


def parse_input(s: str):
    return s


def part_1(input_str: str):
    program = Program()
    program.init_from_str(input_str)
    while True:
        program.execute_next()
        if program.instr_ptr == 28:
            return program.reg[4]


def part_2(input_str: str):
    """
    Working on program decompilation:
      5: e = 0
      6: b = e|0b1 00000000 00000000
      7: e = 678134
      8: f = b % 256
     10: e = 65899*(e+f) % 2^24

        if (b < 256):
            if (e == x):
                halt
            else:
                goto 6

        b = (b >> 8)
        goto 8
    """
    seen_vals_set = set()
    seen_vals = []
    e = 0

    while True:
        b = e | 0b10000000000000000
        e = 678134

        while True:
            e = 65899 * (e + (b % 256)) % (2**24)
            if b < 256:
                if e in seen_vals_set:
                    return seen_vals[-1]
                seen_vals_set.add(e)
                seen_vals.append(e)
                break
            b = (b >> 8)


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(21)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
