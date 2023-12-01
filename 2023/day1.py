import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen""")


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
        data.append(line)
    return data


def part_1(data):
    numeric = '1234567890'
    nums = []
    for line in data:
        chars = [x for x in line if x in numeric]
        nums.append(int(chars[0] + chars[-1]))
    print(f'Part 1: {sum(nums)}')


from typing import List
def index_all(s: str, vals: List[str]):
    locs = dict()
    for val in vals:
        locs[val] = []
        line_idx = 0
        while line_idx < len(s):
            next_occurance = s.find(val, line_idx)
            if next_occurance >= 0:
                locs[val].append(next_occurance)
                line_idx = next_occurance + 1
            else:
                break
    return locs


def part_2(data):
    def convert(s: str):
        if s in ordinals:
            return str(ordinals.index(s) + 1)
        else:
            return str(int(s))

    numeric = '1234567890'
    ordinals = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    vals = list([x for x in numeric]) + ordinals
    final_nums = []
    for line in data:
        ordinal_locs = index_all(line, vals)
        nums = dict()
        for k, v in ordinal_locs.items():
            for x in v:
                nums[x] = k
        numlist = [convert(q[1]) for q in sorted(list(nums.items()), key=lambda p: p[0])]
        final_nums.append(int(numlist[0] + numlist[-1]))

    print(f'Part 2: {sum(final_nums)}')


def main():
    data = read_input(day_number=1, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
