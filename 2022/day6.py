import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    mjqjpqmgbljsphdztnvjfqwrcgsmlb""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    for line in s.splitlines(keepends=False):
        return line


def part_1(s):
    for idx in range(len(s) - 3):
        chars = {s[idx], s[idx+1], s[idx+2], s[idx+3]}
        if len(chars) == 4:
            print(f'Part 1: {idx+4}')
            break


def part_2(s):
    for idx in range(len(s) - 3):
        chars = set([s[idx+i] for i in range(0, 14)])
        if len(chars) == 14:
            print(f'Part 1: {idx+14}')
            break


def main():
    data = read_input(day_number=6, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
