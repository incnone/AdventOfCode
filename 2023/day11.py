import textwrap
from collections import Counter
from itertools import product, combinations


def get_test_input() -> str:
    return textwrap.dedent("""\
    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for row, line in enumerate(s.splitlines(keepends=False)):
        for col, c in enumerate(line):
            if c == '#':
                data.append((col, row))
    return data


def pathlens_with_expansion(data, factor):
    # Find cols/rows with no galaxies
    rows = Counter(d[1] for d in data)
    cols = Counter(d[0] for d in data)

    width = max(cols.keys())
    height = max(rows.keys())

    empty_rows = []
    empty_cols = []

    for col in range(width):
        if col not in cols:
            empty_cols.append(col)
    for row in range(height):
        if row not in rows:
            empty_rows.append(row)

    print(empty_cols)
    print(empty_rows)

    new_data = []
    expand = factor - 1
    for x, y in data:
        new_x = x + sum(expand if c < x else 0 for c in empty_cols)
        new_y = y + sum(expand if r < y else 0 for r in empty_rows)
        new_data.append((new_x, new_y))

    pathlen = 0
    for p1, p2 in combinations(new_data, 2):
        x1, y1 = p1
        x2, y2 = p2
        pathlen += abs(x1 - x2) + abs(y1 - y2)

    return pathlen


def part_1(data):
    print(f'Part 1: {pathlens_with_expansion(data, 2)}')


def part_2(data):
    print(f'Part 2: {pathlens_with_expansion(data, 1000000)}')


def main():
    data = read_input(day_number=11, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
