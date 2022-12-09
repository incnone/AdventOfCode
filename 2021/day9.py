import textwrap
import itertools


def get_test_input() -> str:
    return textwrap.dedent("""\
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678""")


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
        data.append([int(x) for x in line])
    return data


def find_low_points(data):
    low_points = []
    width, height = len(data[0]), len(data)
    for x, y in itertools.product(range(width), range(height)):
        val = data[y][x]
        uval = data[y-1][x] if y > 0 else 999
        dval = data[y+1][x] if y < height - 1 else 999
        lval = data[y][x-1] if x > 0 else 999
        rval = data[y][x+1] if x < width - 1 else 999
        if val < min(uval, dval, lval, rval):
            low_points.append((x, y,))
    return low_points


def find_basin(low_point, data):
    width, height = len(data[0]), len(data)
    to_check = [low_point]
    checked = set(low_point)
    basin = {low_point}
    while to_check:
        x, y = to_check.pop()
        checked.add((x, y,))
        for u, v in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= u < width and 0 <= v < height and (u, v,) not in checked and data[v][u] < 9:
                checked.add((u, v))
                to_check.append((u, v))
                basin.add((u, v))
    return basin


def part_1(data):
    tot = sum(data[y][x]+1 for x, y in find_low_points(data))
    print(f'Part 1: {tot}')


def part_2(data):
    low_points = find_low_points(data)
    basins = []
    for lp in low_points:
        basins.append(find_basin(lp, data))
    basins = sorted(basins, key=lambda b: len(b), reverse=True)
    print(f'Part 2: {len(basins[0])*len(basins[1])*len(basins[2])}')


def main():
    data = read_input(day_number=9, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
