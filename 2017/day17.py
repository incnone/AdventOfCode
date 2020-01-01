from getinput import get_input
import itertools


def part_1(input_str):
    buffer = [0]
    skipval = int(input_str)
    cursor = 0
    for idx in range(1, 2018):
        cursor = ((cursor + skipval) % len(buffer)) + 1
        buffer.insert(cursor, idx)
    return buffer[(cursor + 1) % len(buffer)]


def part_2(input_str):
    skipval = int(input_str)
    buffer_len = 1
    cursor = 0
    last_inserted = None
    for idx in range(1, 50*(10**6)):
        cursor = ((cursor + skipval) % buffer_len) + 1
        buffer_len += 1
        if cursor == 1:
            last_inserted = idx
    return last_inserted


def main():
    input_str = get_input(17)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
