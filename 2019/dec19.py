from intcode import IntcodeProgram
from typing import List, Tuple


class TractorBeamScanner(object):
    def __init__(self, program_code):
        self.program_code = program_code
        self.beam_rows = [(0, 1), (2, 3), (4, 5), (6, 7)]       # type: List[Tuple[int,int]]

    def has_beam(self, loc):
        program = IntcodeProgram.list_program(self.program_code)
        program.io_handler.input_list = list(loc)
        program.execute()
        return bool(program.io_handler.output_list[0])

    def scan_next_row(self):
        y = len(self.beam_rows)
        last_bounds = self.beam_rows[-1]
        x = last_bounds[0]
        scanned_beam = self.has_beam((x, y))
        while not scanned_beam:
            x += 1
            scanned_beam = self.has_beam((x, y))
        start_x = x
        x += last_bounds[1] - last_bounds[0]
        scanned_beam = self.has_beam((x, y))
        while scanned_beam:
            x += 1
            scanned_beam = self.has_beam((x, y))
        self.beam_rows.append((start_x, x))

    def scan_rows(self, num_rows):
        for _ in range(num_rows):
            self.scan_next_row()

    def square_fits(self, square_size):
        return self.beam_rows[-square_size][1] - self.beam_rows[-1][0] >= square_size


def part_1(prog_code_str):
    outputs_1 = ''

    for y in range(0, 50):
        for x in range(0, 50):
            loc = (x, y)
            program = IntcodeProgram.list_program(prog_code_str)
            program.io_handler.input_list = list(loc)
            program.execute()
            if program.io_handler.output_list[0] == 1:
                outputs_1 += '#'
            else:
                outputs_1 += '.'
        outputs_1 += '\n'

    with open('dec_19_beam.txt', 'w') as file:
        file.write(outputs_1)


def part_2(prog_code_str):
    scanner = TractorBeamScanner(prog_code_str)
    scanner.scan_rows(100)
    while not scanner.square_fits(100):
        scanner.scan_next_row()
        num_rows_scanned = len(scanner.beam_rows)
        if num_rows_scanned % 100 == 0:
            print(num_rows_scanned)

    print('Y=', len(scanner.beam_rows) - 100)
    print('X=', scanner.beam_rows[-1])


def puzzleinput():
    with open('input/dec19.txt') as file:
        return file.read().strip('\n')


if __name__ == "__main__":
    part_1(puzzleinput())
    part_2(puzzleinput())
