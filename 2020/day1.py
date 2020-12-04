import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    1721
    979
    366
    299
    675
    1456""")


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
        data.append(int(line.rstrip('\n')))
    return data


def part_1(nums):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print("Part 1: {}".format(nums[i]*nums[j]))


def part_2(nums):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            for k in range(j+1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print("Part 2: {}".format(nums[i]*nums[j]*nums[k]))


def main():
    nums = read_input(day_number=1, test=True)
    part_1(nums)
    part_2(nums)


if __name__ == "__main__":
    main()


