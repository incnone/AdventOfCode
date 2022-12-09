import textwrap
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    R 5
    U 8
    L 8
    D 3
    R 17
    D 10
    L 25
    U 20""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


# def parse_input(s: str):
#     data = []
#     for line in s.splitlines(keepends=False):
#         w = line.split()
#         if w[0] == 'U':
#             data.append(np.array([0, int(w[1])]))
#         elif w[0] == 'D':
#             data.append(np.array([0, -int(w[1])]))
#         elif w[0] == 'R':
#             data.append(np.array([int(w[1]), 0]))
#         elif w[0] == 'L':
#             data.append(np.array([-int(w[1]), 0]))
#     return data


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        w = line.split()
        for _ in range(int(w[1])):
            if w[0] == 'U':
                data.append(np.array([0, 1]))
            elif w[0] == 'D':
                data.append(np.array([0, -1]))
            elif w[0] == 'R':
                data.append(np.array([1, 0]))
            elif w[0] == 'L':
                data.append(np.array([-1, 0]))
    return data


class Rope(object):
    def __init__(self, loc=(0, 0), tail_length=1):
        self.head = np.array(loc)
        self.tail = [np.array(loc) for _ in range(tail_length)]

    def move(self, disp):
        self.head += disp
        self._update(self.head, self.tail[0])
        for i in range(1, len(self.tail)):
            self._update(self.tail[i-1], self.tail[i])

    @staticmethod
    def _update(head, tail):
        diff = head - tail
        if np.amax(np.absolute(diff)) >= 2:
            tail += np.clip(diff, -1, 1)


def part_1(data):
    rope = Rope()
    visited = {(0, 0)}
    for d in data:
        rope.move(d)
        visited.add(tuple(rope.tail[-1]))

    print(f'Part 1: {len(visited)}')


def part_2(data):
    rope = Rope(tail_length=9)
    visited = {(0, 0)}
    for d in data:
        rope.move(d)
        visited.add(tuple(rope.tail[-1]))

    print(f'Part 1: {len(visited)}')


def main():
    data = read_input(day_number=9, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
