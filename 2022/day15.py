import textwrap
import re
from typing import List


def get_test_input() -> str:
    return textwrap.dedent("""\
    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    Sensor at x=9, y=16: closest beacon is at x=10, y=16
    Sensor at x=13, y=2: closest beacon is at x=15, y=3
    Sensor at x=12, y=14: closest beacon is at x=10, y=16
    Sensor at x=10, y=20: closest beacon is at x=10, y=16
    Sensor at x=14, y=17: closest beacon is at x=10, y=16
    Sensor at x=8, y=7: closest beacon is at x=2, y=10
    Sensor at x=2, y=0: closest beacon is at x=2, y=10
    Sensor at x=0, y=11: closest beacon is at x=2, y=10
    Sensor at x=20, y=14: closest beacon is at x=25, y=17
    Sensor at x=17, y=20: closest beacon is at x=21, y=22
    Sensor at x=16, y=7: closest beacon is at x=15, y=3
    Sensor at x=14, y=3: closest beacon is at x=15, y=3
    Sensor at x=20, y=1: closest beacon is at x=15, y=3""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    for line in s.splitlines(keepends=False):
        m = regex.match(line)
        data.append(tuple(int(m.group(i)) for i in range(1, 5)))
    return data


def dist_taxi(p1, p2):
    return sum(abs(a - b) for (a, b) in zip(p1, p2))


def part_1(data, test):
    sensor_dist = dict()
    beacons = set()
    for x, y, a, b in data:
        sensor_dist[(x, y)] = dist_taxi((x, y), (a, b))
        beacons.add((a, b))

    minval = min(loc[0] - r for (loc, r) in sensor_dist.items())
    maxval = max(loc[0] + r for (loc, r) in sensor_dist.items())
    row = 10 if test else 2000000

    num_blocked = 0
    for x in range(minval, maxval+1):
        if (x, row) not in beacons:
            for loc, r in sensor_dist.items():
                if dist_taxi((x, row), loc) <= r:
                    num_blocked += 1
                    break

    print(f'Part 1: {num_blocked}')


def add_interval_to_list(interval_list: List[int], interval):
    left_idx = 0
    right_idx = 0
    new_list = interval_list.copy()
    while left_idx < len(new_list) and new_list[left_idx] < interval[0]:
        left_idx += 1
        right_idx += 1

    while right_idx < len(new_list) and new_list[right_idx] < interval[1]:
        right_idx += 1

    insert_left = (left_idx % 2 == 0)
    insert_right = (right_idx % 2 == 0)
    if insert_left:
        new_list.insert(left_idx, interval[0])
        left_idx += 1
        right_idx += 1

    if insert_right:
        new_list.insert(right_idx, interval[1])

    ans = []
    last = None
    for idx, val in enumerate(list(new_list[:left_idx] + new_list[right_idx:])):
        if idx % 2 == 0 and len(ans) > 0 and (val == ans[-1] or val == ans[-1] + 1):
            ans.pop(-1)
        else:
            ans.append(val)

    return ans


def part_2(data, test):
    size = 20 if test else 4000000
    rows = []
    for _ in range(size+1):
        rows.append([])

    for x, y, a, b in data:
        r = dist_taxi((x, y), (a, b))
        for row in range(y-r, y+r+1):
            if not 0 <= row <= size:
                continue
            rel_row = row - y
            rel_row_half_width = r - abs(rel_row)
            coverage_interval = [x - rel_row_half_width, x + rel_row_half_width]
            rows[row] = add_interval_to_list(rows[row], coverage_interval)

    for y, row in enumerate(rows):
        if len(row) > 2:
            assert len(row) == 4
            assert row[2] == row[1] + 2
            x = row[1] + 1
            print(f'Part 2: {x * 4000000 + y}')


def main():
    test = False
    data = read_input(day_number=15, test=test)
    part_1(data, test)
    part_2(data, test)


if __name__ == "__main__":
    main()
