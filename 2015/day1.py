from getinput import get_input


def part_1(inputstr):
    floor = 0
    for c in inputstr:
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1

    return floor


def part_2(inputstr):
    floor = 0
    for idx, c in enumerate(inputstr):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
        if floor == -1:
            return idx+1

    return None


if __name__ == "__main__":
    inputstr = get_input(1)

    print('Part 1:', part_1(inputstr))
    print('Part 2:', part_2(inputstr))
