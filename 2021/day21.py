import textwrap
import re
from collections import defaultdict


def get_test_input() -> str:
    return textwrap.dedent("""\
    Player 1 starting position: 4
    Player 2 starting position: 8""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    regex = re.compile(r'Player (?P<player>\d+) starting position: (?P<pos>\d+)')
    for line in s.splitlines(keepends=False):
        m = regex.match(line)
        data.append(int(m.groupdict()['pos']))
    return data


class DeterministicDie(object):
    def __init__(self, num_sides):
        self.num_sides = num_sides
        self.val = 1

    def roll(self):
        try:
            return self.val if self.val != 0 else self.num_sides
        finally:
            self.val = (self.val + 1) % self.num_sides


class DiracDice(object):
    def __init__(self, starting_pos, die):
        self.rolls = 0
        self.die = die
        self.player = 0
        self.scores = [0, 0]
        self.pos = starting_pos
        self.board_size = 10
        self.num_rolls_per_turn = 3

    def take_turn(self):
        for _ in range(self.num_rolls_per_turn):
            self.rolls += 1
            self.pos[self.player] = (self.pos[self.player] + self.die.roll()) % self.board_size
        self.scores[self.player] += self.pos[self.player] if self.pos[self.player] != 0 else self.board_size
        self.player = 1-self.player


class RealDiracDice(object):
    def __init__(self, starting_pos):
        self.player = 0
        self.board_size = 10
        self.num_rolls_per_turn = 3
        self.states = defaultdict(lambda: 0)        # map from (score, pos) to number of universes with that state
        self.states[((0, 0), (starting_pos[0] - 1, starting_pos[1] - 1))] = 1
        self.end_states = defaultdict(lambda: 0)
        self.win_score = 21
        self.any_new_universes = True

    def take_turn(self):
        self.any_new_universes = False
        new_states = defaultdict(lambda: 0)
        die_rolls = [
            (3, 1),
            (4, 3),
            (5, 6),
            (6, 7),
            (7, 6),
            (8, 3),
            (9, 1)
        ]
        for state, num_universes in self.states.items():
            score, pos = state
            if max(score) >= self.win_score:
                self.end_states[score] += num_universes
                continue

            self.any_new_universes = True
            if self.player == 0:
                for roll, num in die_rolls:
                    new_pos = ((pos[0] + roll) % 10, pos[1])
                    new_score = (score[0] + (new_pos[0] + 1), score[1])
                    new_states[(new_score, new_pos)] += num_universes*num
            else:
                for roll, num in die_rolls:
                    new_pos = (pos[0], (pos[1] + roll) % 10)
                    new_score = (score[0], score[1] + (new_pos[1] + 1))
                    new_states[(new_score, new_pos)] += num_universes*num

        self.player = 1 - self.player
        self.states = new_states


def part_1(data):
    game = DiracDice(data, DeterministicDie(100))

    while max(game.scores) < 1000:
        game.take_turn()

    print(game.scores[game.player], game.rolls)
    print(f'Part 1: {game.scores[game.player]*game.rolls}')


def part_2(data):
    game = RealDiracDice(data)

    idx = 0
    while game.any_new_universes:
        game.take_turn()
        idx += 1
        print(idx, len(game.states), len(game.end_states))

    p1_wins = sum(n if g[0] >= game.win_score else 0 for g, n in game.end_states.items())
    p2_wins = sum(n if g[1] >= game.win_score else 0 for g, n in game.end_states.items())
    print(f'Part 2: {max(p1_wins, p2_wins)}')


def main():
    data = read_input(day_number=21, test=False)
    print(data)
    #part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
