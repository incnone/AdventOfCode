from getinput import get_input
import itertools


def do_cancels(s):
    skip = False
    t = ''
    for c in s:
        if skip:
            skip = False
            continue
        if c == '!':
            skip = True
        else:
            t += c
    return t


def clean_garbage(s):
    skip = False
    t = ''
    for c in s:
        if not skip and c == '<':
            t += c
            skip = True
        if skip:
            if c == '>':
                skip = False
                t += c
            continue
        t += c
    return t


def get_score(s):
    depth = 0
    total_score = 0
    for c in s:
        if c == '{':
            depth += 1
        elif c == '}':
            total_score += depth
            depth -= 1
    return total_score


def part_1(input_str):
    return get_score(clean_garbage(do_cancels(input_str)))


def part_2(input_str):
    cancelled = do_cancels(input_str)
    removed = clean_garbage(cancelled)
    return len(cancelled) - len(removed)


def main():
    input_str = get_input(9)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
