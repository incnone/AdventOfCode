import textwrap


triplefib_cache = {1: 1, 2: 1, 3: 2}


def get_test_input() -> str:
    return textwrap.dedent("""\
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(int(line))
    data.append(0)
    data = sorted(data)
    data.append(data[-1] + 3)
    return data


def part_1(data):
    num_1 = 0
    num_3 = 0
    for x, y in zip(data[:-1], data[1:]):
        if y - x == 3:
            num_3 += 1
        elif y - x == 1:
            num_1 += 1
    print('Part 1:', num_1*num_3)


def part_2(data):
    total = 1
    running_ct = 1
    for x, y in zip(data[:-1], data[1:]):
        if y - x == 1:
            running_ct += 1
        elif y - x == 3:
            total *= triplefib(running_ct)
            running_ct = 1
    print('Part 2:', total)


def triplefib(n: int):
    if n in triplefib_cache:
        return triplefib_cache[n]
    else:
        val = triplefib(n-1) + triplefib(n-2) + triplefib(n-3)
        triplefib_cache[n] = val
        return val


def main():
    data = read_input(day_number=10, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
