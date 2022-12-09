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
    for line in s.splitlines(keepends=False):
        pass
    return data


def part_1(data):
    pass


def part_2(data):
    pass


def main():
    data = read_input(day_number=0, test=True)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
