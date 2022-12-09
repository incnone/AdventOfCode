import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


class DigitPattern(object):
    digpats = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9'
    }

    def __init__(self, s):
        patterns, digits = s.split('|')
        self.patterns = patterns.split()
        self.digits = digits.split()
        self.mapping = dict()
        self.number = None
        self._find_mapping()
        self._find_number()

    def __str__(self):
        return ' '.join(self.patterns) + ' | ' + ' '.join(self.digits)

    def _find_mapping(self):
        one_letters = ''
        four_letters = ''
        for x in self.patterns:
            if len(x) == 2:
                one_letters = x
            elif len(x) == 4:
                four_letters = x
        counts = dict()
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            counts[letter] = sum(1 if letter in x else 0 for x in self.patterns)
        for let, c in counts.items():
            if c == 4:
                self.mapping[let] = 'e'
            elif c == 6:
                self.mapping[let] = 'b'
            elif c == 9:
                self.mapping[let] = 'f'
            elif c == 7:
                self.mapping[let] = 'd' if let in four_letters else 'g'
            elif c == 8:
                self.mapping[let] = 'c' if let in one_letters else 'a'
            else:
                raise RuntimeError('oops')

        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            assert letter in self.mapping

    def _find_number(self):
        self.number = int(''.join(
            self.digpats[''.join(sorted(self.mapping[x] for x in digit))] for digit in self.digits)
        )


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(DigitPattern(line))
    return data


def part_1(data):
    tot = 0
    for p in data:
        for k in p.digits:
            if len(k) in [2, 3, 4, 7]:
                tot += 1
    print(f'Part 1: {tot}')


def part_2(data):
    print(f'Part 2: {sum(p.number for p in data)}')


def main():
    data = read_input(day_number=8, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
