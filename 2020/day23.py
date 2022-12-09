import textwrap
import time
from collections import deque


def get_test_input() -> str:
    return textwrap.dedent("""\
    389125467""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return list(int(v) for v in s.rstrip('\n'))


# def do_move(cups):
#     # Get the label of the destination cup
#     dest_val = cups[0] - 1
#     if dest_val == 0:
#         dest_val = 9
#     while dest_val in cups[1:4]:
#         dest_val -= 1
#         if dest_val == 0:
#             dest_val = 9
#
#     dest_idx = cups.index(dest_val)
#     return cups[4:dest_idx + 1] + cups[1:4] + cups[dest_idx + 1:] + [cups[0]]


dmp_1 = 0.0
dmp_2 = 0.0
dmp_3 = 0.0
def do_move(cups):
    global dmp_1
    global dmp_2
    global dmp_3
    now = time.time()

    """Source cup is the first cup"""
    num_cups = len(cups)

    orig = cups.popleft()
    to_move = []
    for _ in range(3):
        to_move.append(cups.popleft())

    dest_val = orig - 1
    if dest_val == 0:
        dest_val = num_cups
    while dest_val in to_move:
        dest_val -= 1
        if dest_val == 0:
            dest_val = num_cups

    # - TIMING -
    new_now = time.time()
    dmp_1 += new_now - now
    now = new_now
    # - END TIMING -

    stack = deque()
    try:
        while cups[-1] != dest_val:
            stack.append(cups.pop())
    except IndexError:
        print(dest_val)

    # - TIMING -
    new_now = time.time()
    dmp_2 += new_now - now
    now = new_now
    # - END TIMING -

    while to_move:
        cups.append(to_move.pop(0))
    while stack:
        cups.append(stack.pop())

    cups.append(orig)

    # - TIMING -
    new_now = time.time()
    dmp_3 += new_now - now
    # - END TIMING -


def part_1(cups):
    for _ in range(100):
        do_move(cups)

    while cups[0] != 1:
        cups.append(cups.popleft())
    print('Part 1:', ''.join(str(c) for c in list(cups)[1:]))


def part_2(cups):
    global dmp_1
    global dmp_2
    global dmp_3

    now = time.time()

    cups = deque(cups)
    for x in range(len(cups) + 1, 1000000 + 1):
        cups.append(x)

    for idx in range(50000):
        if idx % 10000 == 0:
            new_now = time.time()
            print(f'{idx} took {new_now - now} seconds')
            now = new_now
        do_move(cups)

    while cups[0] != 1:
        cups.append(cups.popleft())

    cups.popleft()
    c1 = cups.popleft()
    c2 = cups.popleft()
    print('Part 2:', c1*c2)
    print(dmp_1, dmp_2, dmp_3)


def main():
    cups = deque(read_input(day_number=23, test=True))
    # part_1(cups)
    part_2(cups)


if __name__ == "__main__":
    main()
