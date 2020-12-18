import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    35
    20
    15
    25
    47
    40
    62
    55
    65
    95
    102
    117
    150
    182
    127
    219
    299
    277
    309
    576""")


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
    return data


def part_1(data):
    preamble_size = 25
    for idx in range(preamble_size, len(data)):
        found_sum = False
        for x in range(idx - preamble_size, idx):
            for y in range(x, idx):
                if data[idx] == data[x] + data[y]:
                    found_sum = True
        if not found_sum:
            print('Part 1:', data[idx])


def part_2(data):
    invalid_sum = 1124361034
    for idx in range(len(data)):
        partial_sum = data[idx]
        for jdx in range(idx + 1, len(data)):
            partial_sum += data[jdx]
            if partial_sum == invalid_sum:
                print('Part 2:', min(data[idx:jdx+1]) + max(data[idx:jdx+1]))
                return
            elif partial_sum > invalid_sum:
                break


def main():
    data = read_input(day_number=9, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
