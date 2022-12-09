import textwrap
import itertools
from typing import List, Optional


def get_test_input() -> str:
    return textwrap.dedent("""\
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526""")


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
        data.append(int(x) for x in line)
    return data


class OctoGrid(object):
    def __init__(self, data):
        self.data = list(list(x for x in row) for row in data)  # type: List[List[Optional[int]]]
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.flashes = 0
        self.all_flashed = False

    def __str__(self):
        return '\n'.join(''.join(str(x) for x in row) for row in self.data)

    def step(self):
        for x, y in itertools.product(range(self.width), range(self.height)):
            self.data[y][x] += 1
        any_flash = True
        while any_flash:
            any_flash = False
            for x, y in itertools.product(range(self.width), range(self.height)):
                if self.data[y][x] is not None and self.data[y][x] > 9:
                    self.data[y][x] = None
                    any_flash = True
                    self.flashes += 1
                    for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                        if 0 <= x+i < self.width and 0 <= y+j < self.height and self.data[y+j][x+i] is not None:
                            self.data[y+j][x+i] += 1

        self.all_flashed = True
        for x, y in itertools.product(range(self.width), range(self.height)):
            if self.data[y][x] is None:
                self.data[y][x] = 0
            else:
                self.all_flashed = False


def part_1(data):
    grid = OctoGrid(data)
    for _ in range(100):
        grid.step()
    print(f'Part 1: {grid.flashes}')


def part_2(data):
    grid = OctoGrid(data)
    step = 0
    while not grid.all_flashed:
        grid.step()
        step += 1
    print(f'Part 2: {step}')


def main():
    data = read_input(day_number=11, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
