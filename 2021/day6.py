import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    3,4,3,1,2""")


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


def fish_after(data, num_days):
    cache = [0, 1, 1, 1, 1, 1, 1, 1, 2]
    for n in range(len(cache), num_days + 1):
        cache.append(cache[n-7] + cache[n-9] + 1)
    num_fish = 0
    for fish in data:
        num_fish += 1 + cache[num_days - fish]
    return num_fish


def part_1(data):
    print(f'Part 1: {fish_after(data, 80)}')


def part_2(data):
    print(f'Part 2: {fish_after(data, 256)}')


def main():
    data = read_input(day_number=6, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
