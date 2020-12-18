import textwrap


class Seat(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    @property
    def seat_id(self):
        return self.row*8 + self.col


def get_test_input() -> str:
    return textwrap.dedent("""\
    """)


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
        col = int(line[7:10].replace('L', '0').replace('R', '1'), 2)
        data.append(Seat(row, col))
    return data


def part_1(data):
    max_id_seat = max(data, key=lambda d: d.seat_id)
    print('Part 1:', max_id_seat.seat_id)


def part_2(data):
    data = sorted(data, key=lambda d: d.seat_id)
    for x, y in zip(data, data[1:]):
        if y.seat_id - x.seat_id == 2:
            print('Part 2:', y.seat_id - 1)


def main():
    data = read_input(day_number=5, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
