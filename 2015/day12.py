from getinput import get_input
import re


def get_digit_sum(big_str):
    digits = re.findall(r"-?[\d]+", big_str)
    return sum(int(v) for v in digits)


def part_1(big_str):
    return get_digit_sum(big_str)


def get_weirdval(big_str):
    subobjs = []

    open_brace = None
    brace_level = 0
    for idx, c in enumerate(big_str):
        if c == '{' and idx > 0:
            if brace_level == 0:
                open_brace = idx
            brace_level += 1
        elif c == '}' and idx < len(big_str) - 1:
            brace_level -= 1
            if brace_level == 0:
                subobjs.append((open_brace, idx))

    total = 0
    remaining_str = ''.join(c for idx, c in enumerate(big_str) if not any(x <= idx <= y for x, y in subobjs))
    if ':"red"' not in remaining_str:
        total += get_digit_sum(remaining_str)
        for x, y in subobjs:
            total += get_weirdval(big_str[x:y+1])
    return total


def part_2(big_str):
    return get_weirdval(big_str)


if __name__ == "__main__":
    big_str = get_input(day=12)

    print('Part 1:', part_1(big_str))
    print('Part 2:', part_2(big_str))
