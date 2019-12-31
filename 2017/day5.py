from getinput import get_input
import itertools


def parse_input(s):
    return list(int(w) for w in s.splitlines(keepends=False))


def part_1(input_str):
    arr = parse_input(input_str)
    cursor = 0
    steps = 0
    while 0 <= cursor < len(arr):
        val = arr[cursor]
        arr[cursor] += 1
        cursor += val
        steps += 1
    return steps


def part_2(input_str):
    arr = parse_input(input_str)
    cursor = 0
    steps = 0
    while 0 <= cursor < len(arr):
        val = arr[cursor]
        arr[cursor] += 1 if val < 3 else -1
        cursor += val
        steps += 1
    return steps


def main():
    input_str = get_input(5)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
