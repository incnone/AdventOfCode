import textwrap
from functools import reduce


# Stole this chinese remainder code from rosettacode
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def next_multiple_above(n: int, mult: int):
    return (n//mult + 1)*mult


def get_test_input() -> str:
    return textwrap.dedent("""\
    939
    7,13,x,x,59,x,31,19""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    lines = s.splitlines()
    for bus in lines[1].split(','):
        data.append(int(bus) if bus != 'x' else 0)
    return int(lines[0]), data


def part_1(timestamp, data):
    bustimes = dict()
    for bus in data:
        if bus == 0:
            continue
        bustimes[bus] = next_multiple_above(timestamp, bus)
    bus, nexttime = min(bustimes.items(), key=lambda p: p[1])
    print('Part 1:', bus*(nexttime - timestamp))


def part_2(data):
    a = []
    n = []
    for idx, bus in enumerate(data):
        if bus != 0:
            a.append(-idx)
            n.append(bus)
    print('Part 2:', chinese_remainder(n, a))


def main():
    timestamp, data = read_input(day_number=13, test=False)
    part_1(timestamp, data)
    part_2(data)


if __name__ == "__main__":
    main()
