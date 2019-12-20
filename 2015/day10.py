from getinput import get_input
import itertools


def parse_input(big_str):
    pass


def look_and_say(seq):
    result = ''
    idx = 0
    while idx < len(seq):
        jdx = idx
        while jdx < len(seq) and seq[jdx] == seq[idx]:
            jdx += 1
        num_things = jdx - idx
        result += str(num_things) + seq[idx]
        idx = jdx
    return result


def part_1(seq):
    print(0, seq)
    for x in range(40):
        seq = look_and_say(seq)
        print(x+1)
    return len(seq)


def part_2(seq):
    print(0, seq)
    for x in range(50):
        seq = look_and_say(seq)
        print(x+1)
    return len(seq)


if __name__ == "__main__":
    the_seq = get_input(day=10)

    print('Part 1:', part_1(the_seq))
    print('Part 2:', part_2(the_seq))
