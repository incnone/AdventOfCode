def read_input(day_num: int):
    nums = []
    filename = 'input/dec{}.txt'.format(day_num)
    with open(filename, 'r') as file:
        for line in file:
            nums.append(int(line.rstrip('\n')))
    return nums


def part_1():
    nums = read_input(1)
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print("Part 1: {}".format(nums[i]*nums[j]))


def part_2():
    nums = read_input(1)
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            for k in range(j+1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print("Part 2: {}".format(nums[i]*nums[j]*nums[k]))


if __name__ == "__main__":
    part_1()
    part_2()
