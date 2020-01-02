from getinput import get_input
import itertools
import textwrap


def get_power_level(x, y, grid_serial_number):
    rack_id = x + 10
    return ((rack_id*y + grid_serial_number)*rack_id % 1000) // 100 - 5


def part_1(input_str: str):
    serial_number = int(input_str)
    grid_size = 300
    power_levels = list(
        list(get_power_level(x, y, serial_number) for x in range(1, grid_size+1))
        for y in range(1, grid_size+1)
    )

    max_power_level = -999999999
    max_x = max_y = None
    for x, y in itertools.product(range(1, grid_size-1), range(1, grid_size-1)):
        pwr_level = sum(power_levels[b-1][a-1] for a, b in itertools.product(range(x, x+3), range(y, y+3)))
        if pwr_level > max_power_level:
            max_power_level = pwr_level
            max_x, max_y = x, y
    return '{},{}'.format(max_x, max_y)


def part_2(input_str: str):
    # Quite slow. Could probably be made more efficient by storing results of subsquare computations.
    serial_number = int(input_str)
    grid_size = 300
    power_levels = list(
        list(get_power_level(x, y, serial_number) for x in range(1, grid_size+1))
        for y in range(1, grid_size+1)
    )

    max_power_level = -999999999
    max_x = max_y = max_sq_size = None
    last_x = None
    for x, y in itertools.product(range(1, grid_size-1), range(1, grid_size-1)):
        if x != last_x:
            print(x, max_power_level)
            last_x = x
        pwr_level = power_levels[y-1][x-1]
        for sq_size in range(2, grid_size - max(x-1, y-1)):
            pwr_level = pwr_level + \
                        sum(power_levels[(y-1)+(sq_size-1)][a-1] for a in range(x, x+sq_size-1)) + \
                        sum(power_levels[b-1][(x-1)+(sq_size-1)] for b in range(y, y+sq_size))

            if pwr_level > max_power_level:
                max_power_level = pwr_level
                max_x, max_y, max_sq_size = x, y, sq_size

    return '{},{},{} (Power={})'.format(max_x, max_y, max_sq_size, max_power_level)


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(11)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
