import textwrap
import string


class AnswerGroup(object):
    def __init__(self, s: str):
        self.num_people = 0
        self.answers = []
        for line in s.splitlines():
            self.num_people += 1
            self.answers.append(line)

    def num_all_yes(self):
        yeses = dict()
        for c in string.ascii_lowercase:
            yeses[c] = True
        for s in self.answers:
            for c in string.ascii_lowercase:
                if c not in s:
                    yeses[c] = False
        num = sum([1 if v else 0 for v in yeses.values()])
        return num

    def num_any_yes(self):
        yeses = dict()
        for c in string.ascii_lowercase:
            yeses[c] = False
        for s in self.answers:
            for c in string.ascii_lowercase:
                if c in s:
                    yeses[c] = True
        num = sum([1 if v else 0 for v in yeses.values()])
        return num


def get_test_input() -> str:
    return textwrap.dedent("""\
    abc
    
    a
    b
    c
    
    ab
    ac
    
    a
    a
    a
    a
    
    b""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for group in s.split('\n\n'):
        data.append(AnswerGroup(group))
    return data


def part_1(data):
    total = 0
    for group in data:
        total += group.num_any_yes()
    print('Part 1:', total)


def part_2(data):
    total = 0
    for group in data:
        total += group.num_all_yes()
    print('Part 2:', total)


def main():
    data = read_input(day_number=6, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
