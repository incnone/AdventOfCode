import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010""")


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
        data.append(line)
    return data


def part_1(data):
    newdata = []
    for line in data:
        digits = []
        for i in line:
            digits.append(int(i))
        newdata.append(digits)

    size = len(newdata[0])
    gamma = []
    epsilon = []
    for i in range(size):
        num_ones = 0
        num_zeros = 0
        for entry in newdata:
            if entry[i] == 1:
                num_ones += 1
            elif entry[i] == 0:
                num_zeros += 1
        if num_zeros > num_ones:
            gamma.append(0)
            epsilon.append(1)
        elif num_ones > num_zeros:
            gamma.append(1)
            epsilon.append(0)
        else:
            print("unexpected")

    print(f'Part 1: gamma: {gamma}, epsilon: {epsilon}')
    print(0b000101011101*0b111010100010)


def part_2(data):
    newdata = []
    for line in data:
        digits = ()
        for i in line:
            digits += (int(i),)
        newdata.append(digits)
    size = len(newdata[0])

    o2_elts = set(newdata)
    for i in range(size):
        num_ones = 0
        num_zeros = 0
        for elt in o2_elts:
            if elt[i] == 0:
                num_zeros += 1
            elif elt[i] == 1:
                num_ones += 1

        more_common_val = 1 if num_ones >= num_zeros else 0
        o2_elts = set([x for x in o2_elts if x[i] == more_common_val])
        if len(o2_elts) == 1:
            break

    co2_elts = set(newdata)
    for i in range(size):
        num_ones = 0
        num_zeros = 0
        for elt in co2_elts:
            if elt[i] == 0:
                num_zeros += 1
            elif elt[i] == 1:
                num_ones += 1

        less_common_val = 0 if num_ones >= num_zeros else 1
        co2_elts = set([x for x in co2_elts if x[i] == less_common_val])
        if len(co2_elts) == 1:
            break

    print(o2_elts)
    print(co2_elts)
    print(f'Part 2: {0b000001111101*0b111100010100}')


def main():
    data = read_input(day_number=3, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
