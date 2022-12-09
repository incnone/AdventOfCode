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
        p1, p2 = line.split(',')
        n1 = tuple(int(x) for x in p1.split('-'))
        n2 = tuple(int(x) for x in p2.split('-'))
        data.append((n1, n2))
    return data


def part_1(data):
    n = 0
    for t1, t2 in data:
        if (t1[0] <= t2[0] and t1[1] >= t2[1]) or (t1[0] >= t2[0] and t1[1] <= t2[1]):
            n += 1
    print(f'Part 1: {n}')


def part_2(data):
    n = 0
    for t1, t2 in data:
        if (t1[0] <= t2[0] <= t1[1]) or (t1[0] <= t2[1] <= t1[1]) or (t2[0] <= t1[0] and t1[1] <= t2[1]):
            n += 1
    print(f'Part 2: {n}')


def main():
    data = read_input(day_number=4, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
