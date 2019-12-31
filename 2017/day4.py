from getinput import get_input
from collections import Counter


def valid_password_1(s):
    words = set()
    for word in s.split():
        if word in words:
            return False
        words.add(word)
    return True


def valid_password_2(s):
    words = []
    for word in s.split():
        cword = Counter(word)
        if cword in words:
            return False
        words.append(cword)
    return True


def part_1(input_str):
    return sum(1 if valid_password_1(s) else 0 for s in input_str.splitlines(keepends=False))


def part_2(input_str):
    return sum(1 if valid_password_2(s) else 0 for s in input_str.splitlines(keepends=False))


def main():
    input_str = get_input(4)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
