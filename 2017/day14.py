from getinput import get_input
import itertools
from knothash import knot_hash
from pairs import Direction, add_dir


def to_bits(hash_str):
    return ''.join('{:0>4}'.format(bin(int(c, 16))[2:]) for c in hash_str)


def part_1(input_str):
    total = 0
    for idx in range(128):
        total += sum(1 for c in to_bits(knot_hash('{}-{}'.format(input_str, idx))) if c == '1')
    return total


def get_group(start, grid):
    group = {start}
    to_check = [start]
    while to_check:
        loc = to_check.pop()
        for d in Direction:
            neighbor = add_dir(loc, d)
            if neighbor in group:
                continue
            if not (0 <= neighbor[0] < 128 and 0 <= neighbor[1] < 128):
                continue
            if grid[neighbor[1]][neighbor[0]]:
                group.add(neighbor)
                to_check.append(neighbor)
    return group


def part_2(input_str):
    grid = []
    for idx in range(128):
        grid.append(list(True if c == '1' else False for c in to_bits(knot_hash('{}-{}'.format(input_str, idx)))))

    groups = []
    for x, y in itertools.product(range(128), range(128)):
        if not grid[y][x]:
            continue
        if not any((x, y) in g for g in groups):
            groups.append(get_group((x, y), grid))
    return len(groups)


def main():
    input_str = get_input(14)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
