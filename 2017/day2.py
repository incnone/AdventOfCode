from getinput import get_input
import itertools


def parse_input(s):
    return list(list(int(x) for x in line.split()) for line in s.splitlines(keepends=False))


def part_1(input_str):
    arr = parse_input(input_str)
    return sum(max(row) - min(row) for row in arr)


def part_2(input_str):
    arr = parse_input(input_str)
    tot = 0
    for row in arr:
        for x, y in itertools.combinations(row, 2):
            if x % y == 0:
                tot += x // y
                break
            elif y % x == 0:
                tot += y // x
                break
    return tot


def main():
    input_str = get_input(2)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
