import textwrap
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    vals = {
        '.': 0,
        '>': 1,
        'v': 2
    }

    for line in s.splitlines(keepends=False):
        data.append(list(vals[s] for s in line))
    return np.array(data, dtype=np.byte)


def advance_east(cukes: np.array):
    any_moved = False

    # Go through row by row advancing the east-facing cukes
    for row in range(cukes.shape[0]):
        move_last = (cukes[row, 0] == 0) and (cukes[row, -1] == 1)
        skip_next = False

        for col in range(cukes.shape[1] - 1):
            if skip_next:
                skip_next = False
                continue
            if cukes[row, col] == 1 and cukes[row, col+1] == 0:
                cukes[row, col] = 0
                cukes[row, col+1] = 1
                skip_next = True
                any_moved = True

        if move_last:
            cukes[row, -1] = 0
            cukes[row, 0] = 1
            any_moved = True

    return any_moved


def advance_south(cukes: np.array):
    any_moved = False

    # Go through column by column advancing the south-facing cukes
    for col in range(cukes.shape[1]):
        move_last = (cukes[0, col] == 0) and (cukes[-1, col] == 2)
        skip_next = False

        for row in range(cukes.shape[0] - 1):
            if skip_next:
                skip_next = False
                continue
            if cukes[row, col] == 2 and cukes[row+1, col] == 0:
                cukes[row, col] = 0
                cukes[row+1, col] = 2
                row += 1
                skip_next = True
                any_moved = True

        if move_last:
            cukes[-1, col] = 0
            cukes[0, col] = 2
            any_moved = True

    return any_moved


def advance(cukes: np.array):
    any_moved = advance_east(cukes)
    any_moved |= advance_south(cukes)
    return any_moved


def get_str(cukes: np.array):
    d = {
        0: '.',
        1: '>',
        2: 'v'
    }

    return '\n'.join(''.join(d[v] for v in row) for row in cukes)


def part_1(data):
    any_moved = True
    num_moves = 0

    while any_moved:
        any_moved = advance(data)
        num_moves += 1

        if num_moves % 10 == 0:
            print(f'Step {num_moves}')

    print(f'Part 1: {num_moves}')


def part_2(data):
    pass


def main():
    data = read_input(day_number=25, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
