from getinput import get_input
from collections import Counter


def is_nice_p1(s):
    counter = Counter(s)

    # Needs at least 3 vowels
    if sum(n for c, n in counter.items() if c in 'aeiou') < 3:
        return False

    # Needs a doubled letter
    if all(c != d for c, d in zip(s, s[1:])):
        return False

    # Don't contain bad substrings
    if any((c in s) for c in ['ab', 'cd', 'pq', 'xy']):
        return False

    return True


def is_nice_p2(s):
    # Needs a doubled letter pair without repeats
    last_pair = None
    pairs = set()
    for c, d in zip(s, s[1:]):
        if c+d == last_pair:
            last_pair = None
            continue
        elif c+d in pairs:
            break
        else:
            last_pair = c+d
            pairs.add(c+d)
    else:
        return False

    # Don't contain bad substrings
    if all(c != d for c, d in zip(s, s[2:])):
        return False

    return True


def part_1(big_str):
    return sum(1 for s in big_str.splitlines(keepends=False) if is_nice_p1(s))


def part_2(big_str):
    return sum(1 for s in big_str.splitlines(keepends=False) if is_nice_p2(s))


if __name__ == "__main__":
    input_str = get_input(day=5)

    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))
