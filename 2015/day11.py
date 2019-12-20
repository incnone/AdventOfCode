from getinput import get_input
import itertools


def next_password(password):
    def _increment(idx, password):
        next_c = chr(ord(password[idx]) + 1)
        if next_c == chr(ord('z') + 1):
            next_c = 'a'
        incremented_password = password[:idx] + next_c + password[idx+1:]
        if next_c == 'a':
            incremented_password = _increment(idx-1, incremented_password)
        return incremented_password

    return _increment(len(password) - 1, password)


def valid_password(password):
    if not any(ord(c) == ord(b)+1 == ord(a)+2 for a, b, c in zip(password, password[1:], password[2:])):
        return False

    if any(x in ['i', 'o', 'l'] for x in password):
        return False

    skip = 0
    pairs = 0
    for c, d in zip(password, password[1:]):
        if skip > 0:
            skip -= 1
            continue
        if c == d:
            pairs += 1
            skip = 1

    if pairs < 2:
        return False

    return True


def next_valid_password(password):
    next_pass = next_password(password)
    while not valid_password(next_pass):
        next_pass = next_password(next_pass)
    return next_pass


def part_1(password):
    return next_valid_password(password)


def part_2(password):
    return next_valid_password(next_valid_password(password))


if __name__ == "__main__":
    the_pass = get_input(day=11).strip('\n')

    print('Part 1:', part_1(the_pass))
    print('Part 2:', part_2(the_pass))
