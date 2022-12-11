import textwrap
import numpy as np


def get_test_input() -> str:
    num = 3
    if num == 1:
        return textwrap.dedent("""\
        -1,2,2,0
        0,0,2,-2
        0,0,0,-2
        -1,2,0,0
        -2,-2,-2,2
        3,0,2,-1
        -1,3,2,2
        -1,0,-1,0
        0,2,1,-2
        3,0,0,0""")
    elif num == 2:
        return textwrap.dedent("""\
        1,-1,0,1
        2,0,-1,0
        3,2,-1,0
        0,0,3,1
        0,0,-1,-1
        2,3,-2,0
        -2,2,0,0
        2,-2,0,-1
        1,-1,0,-1
        3,2,0,2""")
    elif num == 3:
        return textwrap.dedent("""\
        1,-1,-1,-2
        -2,-2,0,1
        0,2,1,3
        -2,3,-2,1
        0,2,3,-2
        -1,-1,1,-2
        0,-2,-1,0
        -2,2,3,-1
        1,2,2,0
        -1,-2,0,-2""")


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
        data.append(tuple(int(x) for x in line.split(',')))
    return data


def dist(t1, t2):
    return sum(abs(x - y) for x, y in zip(t1, t2))


def part_1(data):
    searched = set()
    components = 0

    # Find a new component
    for t in data:
        if t in searched:
            continue

        components += 1
        searched.add(t)
        cur_stack = [t]

        while cur_stack:
            s = cur_stack[-1]
            cur_stack.pop(-1)
            searched.add(s)

            for q in data:
                if q in searched:
                    continue
                if dist(q, s) <= 3:
                    cur_stack.append(q)

    print(f'Part 1: {components}')


def part_2(data):
    pass


def main():
    data = read_input(day_number=25, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
