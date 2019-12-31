from getinput import get_input
import itertools


def parse_to_tuple(s):
    return tuple(int(w) for w in s.split())


def redistribute(t):
    idx = max(range(len(t)), key=lambda x: (t[x], -x))
    amt = t[idx] // len(t)
    rmd = t[idx] % len(t)
    return tuple([
        (t[jdx] if jdx != idx else 0)
        + amt
        + (1 if (jdx - idx - 1) % len(t) < rmd else 0)
        for jdx in range(len(t))
    ])


def part_1(input_str):
    blocks = parse_to_tuple(input_str)
    seen_blocks = set()
    cycles = 0
    while blocks not in seen_blocks:
        seen_blocks.add(blocks)
        blocks = redistribute(blocks)
        cycles += 1
    return cycles


def part_2(input_str):
    blocks = parse_to_tuple(input_str)
    seen_blocks = dict()
    cycles = 0
    while blocks not in seen_blocks:
        seen_blocks[blocks] = cycles
        blocks = redistribute(blocks)
        cycles += 1
    return cycles - seen_blocks[blocks]


def main():
    input_str = get_input(6)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
