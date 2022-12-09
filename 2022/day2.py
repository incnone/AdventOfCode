import textwrap
from typing import Tuple

choices = {
    'A': 0,
    'B': 1,
    'C': 2,
    'X': 0,
    'Y': 1,
    'Z': 2
}

numtoplay = {
    0: 'X',
    1: 'Y',
    2: 'Z'
}


def get_test_input() -> str:
    return textwrap.dedent("""\
    A Y
    B X
    C Z""")


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
        data.append(tuple(line.split()))
    return data


def result(t: Tuple[str, str]):

    theirs = choices[t[0]]
    mine = choices[t[1]]

    diff = (mine - theirs) % 3
    if diff == 2:
        diff = -1
    return diff


def linescore(t):
    winscore = (result(t) + 1) * 3
    shapescore = choices[t[1]] + 1
    return winscore + shapescore


def part_1(data):
    print(f'Part 1: {sum([linescore(t) for t in data])}')


def get_p2_play(t):
    theirs = choices[t[0]]
    desired_result = choices[t[1]] - 1
    return numtoplay[(theirs + desired_result) % 3]


def part_2(data):
    print(f'Part 2: {sum([linescore((t[0], get_p2_play(t))) for t in data])}')


def main():
    data = read_input(day_number=2, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
