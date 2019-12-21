import textwrap
from intcode import IntcodeProgram, IOHandlerL2C, IOHandlerS2C


def part_1(program_code):
    io_handler = IOHandlerS2C()
    program = IntcodeProgram(code=program_code, io_handler=io_handler)

    io_handler.input_str = textwrap.dedent("""\
    NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK
    """)

    program.execute()


def part_2(program_code):
    io_handler = IOHandlerS2C()
    program = IntcodeProgram(code=program_code, io_handler=io_handler)

    io_handler.input_str = textwrap.dedent("""\
    OR C J
    AND B J
    AND A J
    NOT J J
    AND D J
    OR E T
    OR H T
    AND T J
    RUN
    """)

    program.execute()


if __name__ == '__main__':
    with open('input/dec21.txt', 'r') as file:
        the_program_code = file.read()

    print("Part 1:")
    part_1(the_program_code)
    print("\nPart 2:")
    part_2(the_program_code)
