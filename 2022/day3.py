import textwrap
import string


def get_test_input() -> str:
    return textwrap.dedent("""\
    """)


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
        data.append(line)
    return data


def part_1(data):
    prio = 0
    for s in data:
        s1, s2 = s[:len(s)/2], s[len(s)/2:]
        for c in string.ascii_lowercase:
            if c in s1 and c in s2:
                prio += ord(c) - ord('a') + 1
        for c in string.ascii_uppercase:
            if c in s1 and c in s2:
                prio += ord(c) - ord('A') + 27

    print(f'Part 1: {prio}')


def part_2(data):
    idx = 0
    prio = 0
    while idx < len(data):
        s1, s2, s3 = data[idx], data[idx+1], data[idx+2]

        for c in string.ascii_lowercase:
            if c in s1 and c in s2 and c in s3:
                prio += ord(c) - ord('a') + 1
        for c in string.ascii_uppercase:
            if c in s1 and c in s2 and c in s3:
                prio += ord(c) - ord('A') + 27

        idx += 3

    print(f'Part 2: {prio}')


def main():
    data = read_input(day_number=3, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
