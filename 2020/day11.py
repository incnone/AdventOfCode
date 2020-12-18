import textwrap
import copy
from typing import List


class SeatGrid(object):
    def __init__(self, s: str):
        self.grid = []  # type: List[str]
        self.stable = False
        for line in s.splitlines():
            self.grid.append(line.rstrip('\n'))

    def get_seat(self, loc):
        if not 0 <= loc[1] < len(self.grid):
            return '.'
        elif not 0 <= loc[0] < len(self.grid[loc[1]]):
            return '.'
        return self.grid[loc[1]][loc[0]]

    @staticmethod
    def set_seat(grid, loc, val):
        grid[loc[1]] = grid[loc[1]][:loc[0]] + val + grid[loc[1]][loc[0]+1:]

    @staticmethod
    def adjacent_pos(loc):
        return [
            (loc[0] - 1, loc[1] - 1),
            (loc[0], loc[1] - 1),
            (loc[0] + 1, loc[1] - 1),
            (loc[0] - 1, loc[1]),
            (loc[0] + 1, loc[1]),
            (loc[0] - 1, loc[1] + 1),
            (loc[0], loc[1] + 1),
            (loc[0] + 1, loc[1] + 1),
        ]

    def get_num_seen_occupied(self, loc):
        dirs = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]
        count = 0
        for d in dirs:
            new_loc = (loc[0] + d[0], loc[1] + d[1])
            while 0 <= new_loc[1] < len(self.grid) and 0 <= new_loc[0] < len(self.grid[new_loc[1]]) \
                    and self.grid[new_loc[1]][new_loc[0]] == '.':
                new_loc = (new_loc[0] + d[0], new_loc[1] + d[1])
            if self.get_seat(new_loc) == '#':
                count += 1
                continue
        return count

    def step(self):
        new_grid = copy.deepcopy(self.grid)
        for row_num, row in enumerate(self.grid):
            for col_num, val in enumerate(row):
                if val == '.':
                    continue
                elif val == 'L':
                    any_occd = False
                    for loc in self.adjacent_pos((col_num, row_num)):
                        if self.get_seat(loc) == '#':
                            any_occd = True
                    if not any_occd:
                        self.set_seat(new_grid, (col_num, row_num), '#')
                elif val == "#":
                    num_occd = 0
                    for loc in self.adjacent_pos((col_num, row_num)):
                        if self.get_seat(loc) == '#':
                            num_occd += 1
                    if num_occd >= 4:
                        self.set_seat(new_grid, (col_num, row_num), 'L')
        if new_grid == self.grid:
            self.stable = True
        self.grid = new_grid

    def step_2(self):
        new_grid = copy.deepcopy(self.grid)
        for row_num, row in enumerate(self.grid):
            for col_num, val in enumerate(row):
                if val == '.':
                    continue
                elif val == 'L':
                    if self.get_num_seen_occupied((col_num, row_num)) == 0:
                        self.set_seat(new_grid, (col_num, row_num), '#')
                elif val == "#":
                    x = self.get_num_seen_occupied((col_num, row_num))
                    if self.get_num_seen_occupied((col_num, row_num)) >= 5:
                        self.set_seat(new_grid, (col_num, row_num), 'L')
        if new_grid == self.grid:
            self.stable = True
        self.grid = new_grid

    def step_until_stable(self):
        while not self.stable:
            self.step()

    def step_2_until_stable(self):
        while not self.stable:
            self.step_2()

    def num_occupied(self):
        num_occd = 0
        for row_num, row in enumerate(self.grid):
            for col_num, val in enumerate(row):
                if val == '#':
                    num_occd += 1
        return num_occd

    def __str__(self):
        return '\n'.join(s for s in self.grid)


def get_test_input() -> str:
    return textwrap.dedent("""\
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return SeatGrid(s)


def part_1(data):
    data.step_until_stable()
    print('Part 1:', data.num_occupied())


def part_2(data):
    data.step_2_until_stable()
    print('Part 2:', data.num_occupied())


def main():
    data = read_input(day_number=11, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
