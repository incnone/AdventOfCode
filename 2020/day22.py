import textwrap


class CombatGame(object):
    def __init__(self, deck_1, deck_2):
        self.deck_1 = deck_1
        self.deck_2 = deck_2

    def __str__(self):
        return f'Player 1: {self.deck_1}\nPlayer 2: {self.deck_2}'

    def play_round(self):
        p1, p2 = self.deck_1.pop(0), self.deck_2.pop(0)
        if p1 > p2:
            self.deck_1 += [p1, p2]
        else:
            self.deck_2 += [p2, p1]

    def play(self):
        while self.deck_1 and self.deck_2:
            self.play_round()


class RecursiveCombatGame(object):
    def __init__(self, deck_1, deck_2):
        self.deck_1 = deck_1
        self.deck_2 = deck_2
        self.deck_priors = set()
        self.winner = None

    def __str__(self):
        return f'Player 1: {self.deck_1}\nPlayer 2: {self.deck_2}'

    def play_round(self):
        # Don't play if someone's already won
        if self.winner:
            return

        # Check for a prior configuration
        if (tuple(self.deck_1), tuple(self.deck_2)) in self.deck_priors:
            self.winner = 1
        self.deck_priors.add((tuple(self.deck_1), tuple(self.deck_2)))

        # Play the top cards
        p1, p2 = self.deck_1.pop(0), self.deck_2.pop(0)
        p1_wins_round = None

        # Recursive combat rule
        if len(self.deck_1) >= p1 and len(self.deck_2) >= p2:
            subgame = RecursiveCombatGame(list(self.deck_1[:p1]), list(self.deck_2[:p2]))
            subgame.play()
            p1_wins_round = (subgame.winner == 1)
        else:
            p1_wins_round = p1 > p2

        if p1_wins_round:
            self.deck_1 += [p1, p2]
        else:
            self.deck_2 += [p2, p1]

        if not self.deck_1:
            self.winner = 2
        elif not self.deck_2:
            self.winner = 1

    def play(self):
        while self.winner is None:
            self.play_round()


def score(deck):
    tot = 0
    for idx, card in enumerate(reversed(deck)):
        tot += (idx+1)*card
    return tot


def get_test_input() -> str:
    return textwrap.dedent("""\
    Player 1:
    9
    2
    6
    3
    1
    
    Player 2:
    5
    8
    4
    7
    10""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for player_deck in s.split('\n\n'):
        deck = []
        for line in (player_deck.splitlines(keepends=False))[1:]:
            deck.append(int(line))
        data.append(deck)
    return data


def part_1(data):
    game = CombatGame(data[0], data[1])
    game.play()
    if game.deck_1:
        print('Part 1:', score(game.deck_1))
    else:
        print('Part 1:', score(game.deck_2))


def part_2(data):
    game = RecursiveCombatGame(data[0], data[1])
    game.play()
    if game.winner == 1:
        print('Part 2:', score(game.deck_1))
    else:
        print('Part 2:', score(game.deck_2))


def main():
    data = read_input(day_number=22, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
