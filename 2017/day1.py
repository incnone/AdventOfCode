from getinput import get_input
import itertools


def captcha(s):
    total = int(s[0]) if s[0] == s[-1] else 0
    for s1, s2 in zip(s, s[1:]):
        if s1 == s2:
            total += int(s1)
    return total


def captcha_2(s):
    total = 0
    k = len(s) // 2
    for s1, s2 in zip(s, s[k:] + s[:k]):
        if s1 == s2:
            total += int(s1)
    return total


def part_1(input_str):
    return captcha(input_str)


def part_2(input_str):
    return captcha_2(input_str)


def main():
    input_str = get_input(1)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
