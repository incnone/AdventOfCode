import textwrap
import math


def get_test_input() -> str:
    return textwrap.dedent("""\
    Time:      7  15   30
    Distance:  9  40  200""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    time_s, distance_s = s.splitlines(keepends=False)
    times = [int(x) for x in time_s.split()[1:]]
    distances = [int(x) for x in distance_s.split()[1:]]
    return times, distances


def num_wins(t, d):
    eps = 10**(-5)
    disc = math.sqrt(t * t - 4 * d)
    low = math.ceil((t - disc) / 2 + eps)
    high = math.floor((t + disc) / 2 - eps)
    return high + 1 - low


def part_1(times, distances):
    total = 1
    for t, d in zip(times, distances):
        total *= num_wins(t, d)

    print(f'Part 1: {total}')


def part_2(times, distances):
    time_s = ''.join(str(s) for s in times)
    dist_s = ''.join(str(s) for s in distances)
    time = int(time_s)
    dist = int(dist_s)
    print(f'Part 2: {num_wins(time, dist)}')


def main():
    times, distances = read_input(day_number=6, test=False)
    part_1(times, distances)
    part_2(times, distances)


if __name__ == "__main__":
    main()
