import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19
    
     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6
    
    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7""")


class BingoBoard(object):
    def __init__(self, s):
        self.board = s
        self.marked = [[False]*5 for _ in range(5)]

    def __str__(self):
        return f'{self.board}, {self.marked}'

    def __repr__(self):
        return str(self)

    def mark(self, num):
        for i in range(5):
            for j in range(5):
                if self.board[j][i] == num:
                    self.marked[j][i] = True

    def completed(self):
        for i in range(5):
            if all(self.marked[j][i] for j in range(5)):
                return True
        for j in range(5):
            if all(self.marked[j][i] for i in range(5)):
                return True
        return False

    def sum_unmarked(self):
        tot = 0
        for i in range(5):
            for j in range(5):
                if not self.marked[j][i]:
                    tot += self.board[j][i]
        return tot


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    boards = []
    lines = s.splitlines(keepends=False)
    numbers = [int(x) for x in lines[0].split(',')]
    current_board = []
    for line in lines[1:]:
        row = [int(x) for x in line.split()]
        if row:
            current_board.append(row)
        else:
            if current_board:
                boards.append(BingoBoard(current_board))
            current_board = []
    if current_board:
        boards.append(BingoBoard(current_board))
    return numbers, boards


def part_1(numbers, boards):
    for n in numbers:
        for b in boards:
            b.mark(n)
        for b in boards:
            if b.completed():
                print(f'Part 1: {b.sum_unmarked() * n}')
                return


def part_2(numbers, boards):
    unwinning_boards = set([b for b in boards])

    for n in numbers:
        for b in boards:
            b.mark(n)
        for b in boards:
            if b.completed() and b in unwinning_boards:
                unwinning_boards.remove(b)
                if len(unwinning_boards) == 0:
                    print(f'Part 2: {n*b.sum_unmarked()}')
                    return


def main():
    numbers, boards = read_input(day_number=4, test=False)
    part_1(numbers, boards)
    part_2(numbers, boards)


if __name__ == "__main__":
    main()
