from getinput import get_input
import itertools


def parse_input(s):
    pipes = dict()
    for line in s.splitlines(keepends=False):
        words = line.split('<->')
        pipes[int(words[0])] = [int(x) for x in words[1].split(',')]
    return pipes


def get_group(start, pipes):
    connected = {start}
    to_check = [start]
    while to_check:
        pipe = to_check.pop()
        for connection in pipes[pipe]:
            if connection not in connected:
                connected.add(connection)
                to_check.append(connection)
    return connected


def part_1(input_str):
    pipes = parse_input(input_str)
    return len(get_group(0, pipes))


def part_2(input_str):
    pipes = parse_input(input_str)
    groups = []
    for pipe in pipes.keys():
        if not any((pipe in g) for g in groups):
            groups.append(get_group(pipe, pipes))
    return len(groups)


def main():
    input_str = get_input(12)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
