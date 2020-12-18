import textwrap
from typing import List


class SpokenNumbers(object):
    def __init__(self, init: List[int]):
        self.most_recent = init[-1]
        self.last_spoken = dict()
        self.num_spoken = len(init)
        for idx, num in enumerate(init[:-1]):
            self.last_spoken[num] = idx

    def speak(self):
        temp = self.most_recent
        if self.most_recent in self.last_spoken:
            self.most_recent = self.num_spoken - self.last_spoken[self.most_recent] - 1
        else:
            self.most_recent = 0
        self.last_spoken[temp] = self.num_spoken - 1
        self.num_spoken += 1

    def __len__(self):
        return self.num_spoken

    def __str__(self):
        return f'{self.most_recent} ({self.num_spoken}): {self.last_spoken}'


def get_test_input() -> str:
    return textwrap.dedent("""\
    0,3,6""")


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
        for num in line.split(','):
            data.append(int(num))
    return SpokenNumbers(data)


def part_1(data):
    num_speaks = 2020
    for _ in range(num_speaks - len(data)):
        data.speak()
    print('Part 1:', data.most_recent)


def part_2(data):
    num_speaks = 30000000
    for _ in range(num_speaks - len(data)):
        data.speak()
    print('Part 1:', data.most_recent)


def main():
    data = read_input(day_number=15, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
