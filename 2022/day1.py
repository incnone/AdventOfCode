import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    """)


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    current_elf = []
    for line in s.splitlines(keepends=False):
        if line == '':
            data.append(current_elf.copy())
            current_elf = []
        else:
            current_elf.append(int(line))
    return data


def part_1(data):
    sums = map(sum, data)
    print(f'Part 1: {max(list(sums))}')


def part_2(data):
    sums = list(map(sum, data))
    sums = sorted(sums, reverse=True)
    print(f'Part 2: {sums[0] + sums[1] + sums[2]}')


def main():
    data = read_input(day_number=1, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
