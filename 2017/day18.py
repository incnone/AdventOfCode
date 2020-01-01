from getinput import get_input
from program import Program


def parse_input(s):
    return s.splitlines(keepends=False)


def part_1(input_str):
    # Stupid backhack here because the architechture of Program for part 2
    # doesn't lend itself to the Part 1 question well
    prog = Program(code=parse_input(input_str))
    prog.linked_program = prog
    while 0 <= prog.cursor < len(prog.code):
        cmd = prog.code[prog.cursor]
        words = cmd.split()
        opcode, params = words[0], words[1:]
        if opcode == 'rcv' and prog.val(params[0]) != 0:
            return prog.received_values[-1]
        prog.execute_next()
    return prog.received_values[0]


def part_2(input_str):
    prog_0 = Program(code=parse_input(input_str))
    prog_1 = Program(code=parse_input(input_str))
    prog_0.linked_program = prog_1
    prog_1.linked_program = prog_0
    prog_0.registers['p'] = 0
    prog_1.registers['p'] = 1
    while prog_0.waiting < 2 or prog_1.waiting < 2:
        prog_0.execute_next()
        prog_1.execute_next()
    return prog_1.num_sent


def main():
    input_str = get_input(18)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
