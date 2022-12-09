import textwrap
import statistics
import math


def get_test_input() -> str:
    return textwrap.dedent("""\
    16,1,2,0,4,2,7,1,2,14""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data = [int(x) for x in line.split(',')]
    return data


def part_1(data):
    med = statistics.median(data)
    assert med.is_integer()
    print(f'Part 1: {sum(abs(x - med) for x in data)}')


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def part_2(data):
    tot = sum(data)

    def deriv_val(m):
        return 2*tot - 2*len(data)*m + sum(sign(x - m) for x in data)

    mean = round(statistics.mean(data))
    while deriv_val(mean) < 0:  # won't work in general
        mean -= 1
    print(f'Part 2: {sum(abs(x - mean)*(abs(x - mean) + 1)/2 for x in data)}')


def main():
    data = read_input(day_number=7, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
