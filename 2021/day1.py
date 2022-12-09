import textwrap
import itertools


def get_test_input() -> str:
    return textwrap.dedent("""\
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263""")


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
        data.append(int(line.rstrip('\n')))
    return data


def part_1(nums):
    increases = 0
    for i, j in zip(nums, nums[1:]):
        if j > i:
            increases += 1
    print(f'Part 1: {increases}')


def part_2(nums):
    increases = 0
    for i, l in zip(nums, nums[3:]):
        if l > i:
            increases += 1
    print(f'Part 2: {increases}')


def main():
    nums = read_input(day_number=1, test=False)
    part_1(nums)
    part_2(nums)


if __name__ == "__main__":
    main()


