from getinput import get_input
from knothash import sparse_knot_hash, knot_hash


def part_1(input_str):
    twist_lengths = [int(x) for x in input_str.split(',')]
    twisted = sparse_knot_hash(twist_lengths, 256)
    return twisted[0]*twisted[1]


def part_2(input_str):
    return knot_hash(input_str)


def main():
    input_str = get_input(10)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
