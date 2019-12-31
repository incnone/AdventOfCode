from getinput import get_input
import itertools


def parse_input(s):
    return tuple(int(line.split()[-1]) for line in s.splitlines(keepends=False))


def get_factors():
    return 16807, 48271


def part_1(input_str):
    gens = list(parse_input(input_str))
    factors = get_factors()
    matches = 0
    for x in range(40*(10**6)):
        # if x % 1000000 == 0:
        #     print(x//1000000, matches)
        for idx, g in enumerate(gens):
            gens[idx] = g * factors[idx] % 2147483647
        if (gens[0] % 65536) == (gens[1] % 65536):
            matches += 1
    return matches


def part_2(input_str):
    gens = list(parse_input(input_str))
    factors = get_factors()
    matches = 0
    for x in range(5*(10**6)):
        # if x % 100000 == 0:
        #     print(x//100000, matches)

        gens[0] = gens[0] * factors[0] % 2147483647
        while gens[0] % 4 != 0:
            gens[0] = gens[0] * factors[0] % 2147483647

        gens[1] = gens[1] * factors[1] % 2147483647
        while gens[1] % 8 != 0:
            gens[1] = gens[1] * factors[1] % 2147483647

        if (gens[0] % 65536) == (gens[1] % 65536):
            matches += 1
    return matches


def main():
    input_str = get_input(15)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
