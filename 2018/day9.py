from getinput import get_input
import itertools
import textwrap
from collections import defaultdict


# def winning_score_slow(players, last_marble):
#     # Straightforward approach
#     score = defaultdict(lambda: 0)
#     marbles = [0]
#     cursor = 0
#     for marble in range(1, last_marble+1):
#         if marble % 10000 == 0:
#             print(marble)
#
#         if marble % 23 == 0:
#             cursor = (cursor - 7) % len(marbles)
#             removed = marbles.pop(cursor)
#             cursor = cursor % len(marbles)
#             score[marble % players] += marble + removed
#         else:
#             cursor = ((cursor + 1) % len(marbles)) + 1
#             marbles.insert(cursor, marble)
#         # print(marble % players, cursor, marbles)
#     return max(score.values())


def winning_score(players, last_marble):
    # Linked list approach (avoids pointless list copying)
    # Curious if there's a more "mathy" solution to this problem that would work even for much larger last marbles
    score = defaultdict(lambda: 0)
    next_marble = list([None]*(last_marble+1))
    prev_marble = list([None]*(last_marble+1))
    next_marble[0] = prev_marble[0] = 0
    cursor = 0
    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            for _ in range(7):
                cursor = prev_marble[cursor]
            past, future = prev_marble[cursor], next_marble[cursor]
            next_marble[past], prev_marble[future] = future, past
            score[marble % players] += marble + cursor
            cursor = future
        else:
            cursor = next_marble[cursor]
            future = next_marble[cursor]
            next_marble[cursor] = prev_marble[future] = marble
            next_marble[marble] = future
            prev_marble[marble] = cursor
            cursor = marble
    return max(score.values())


def parse_input(s: str):
    words = s.split()
    return int(words[0]), int(words[-2])


def part_1(input_str: str):
    # input_str = test_input()
    return winning_score(*parse_input(input_str))


def part_2(input_str: str):
    # input_str = test_input()
    players, last_marble = parse_input(input_str)
    last_marble *= 100
    return winning_score(players, last_marble)


def test_input():
    test_num = 3
    if test_num == 1:
        return textwrap.dedent("""\
        9 players; last marble is worth 25 points""")
    elif test_num == 2:
        return textwrap.dedent("""\
        10 players; last marble is worth 1618 points""")
    elif test_num == 3:
        return textwrap.dedent("""\
        13 players; last marble is worth 7999 points""")


def main():
    input_str = get_input(9)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
