import textwrap
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    0 3 6 9 12 15
    1 3 6 10 15 21
    10 13 16 21 30 45""")


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
        data.append(np.array(list(int(x) for x in line.split())))
    return data


def predict(vals):
    n = vals.shape[0]
    diffs = np.zeros((n-1, n+1))
    diffs[0, :-1] = vals.copy()
    for row in range(1, n-1):
        for col in range(n + 1 - row):
            diffs[row, col] = diffs[row-1, col+1] - diffs[row-1, col]

    diffs[n-2, 2] = diffs[n-2, 1]
    for row in range(n-3, -1, -1):
        diffs[row, n - row] = diffs[row+1, n - row - 1] + diffs[row, n - row - 1]
    return int(diffs[0, n])


def predict_back(vals):
    n = vals.shape[0]
    diffs = np.zeros((n-1, n+1))
    diffs[0, :-1] = vals.copy()
    for row in range(1, n-1):
        for col in range(n + 1 - row):
            diffs[row, col] = diffs[row-1, col+1] - diffs[row-1, col]

    prepends = np.zeros(n)
    for row in range(n-2, -1, -1):
        prepends[row] = diffs[row, 0] - prepends[row + 1]
    return int(prepends[0])


def part_1(data):
    print(f'Part 1: {sum(predict(n) for n in data)}')


def part_2(data):
    print(f'Part 2: {sum(predict_back(n) for n in data)}')


def main():
    data = read_input(day_number=9, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
