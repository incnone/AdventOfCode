import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


class CubeGame(object):
    def __init__(self, s: str):
        self.index = None
        self.pulls = []     # List of (R, G, B) tuples

        a, b = s.split(':')
        self.index = int(a.split()[1].rstrip(':'))
        pulls = b.split(';')
        for pull in pulls:
            items = pull.split(',')
            red = 0
            green = 0
            blue = 0
            for item in items:
                num, color = item.split()
                if color == 'red':
                    red = int(num)
                elif color == 'green':
                    green = int(num)
                elif color == 'blue':
                    blue = int(num)
                else:
                    print(f'Unrecognized color {color}')
            self.pulls.append((red, green, blue))

    def __str__(self):
        return f'Game {self.index}: {self.pulls}'

    def minvalid(self):
        minr = 0
        ming = 0
        minb = 0
        for r, g, b in self.pulls:
            minr = max(r, minr)
            ming = max(g, ming)
            minb = max(b, minb)
        return minr, ming, minb

    def power(self):
        r, g, b = self.minvalid()
        return r*g*b


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(CubeGame(line))
        pass
    return data


def part_1(data):
    maxred = 12
    maxgreen = 13
    maxblue = 14
    sumofvalid = 0
    for game in data:
        validgame = True
        for r, g, b in game.pulls:
            if r > maxred or g > maxgreen or b > maxblue:
                validgame = False
        if validgame:
            sumofvalid += game.index
    print(f'Part 1: {sumofvalid}')


def part_2(data):
    print(f'Part 2: {sum(g.power() for g in data)}')


def main():
    data = read_input(day_number=2, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
