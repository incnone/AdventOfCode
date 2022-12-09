import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(line.split())
    return data


def part_1(data):
    x = 0
    z = 0
    for direction, dist in data:
        if direction == 'forward':
            x += int(dist)
        elif direction == 'up':
            z -= int(dist)
            if z < 0:
                print("unexpected")
        elif direction == 'down':
            z += int(dist)

    print(f'Part 1: {x*z}')


def part_2(data):
    x = 0
    depth = 0
    aim = 0
    for direction, dist in data:
        if direction == 'forward':
            x += int(dist)
            depth += aim*int(dist)
        elif direction == 'up':
            aim -= int(dist)
        elif direction == 'down':
            aim += int(dist)

    print(f'Part 2: {x*depth}')


def main():
    data = read_input(day_number=2, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
