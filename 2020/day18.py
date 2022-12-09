import string
import textwrap
import unittest
from typing import List


def parse_calcstr_ltor(s: str) -> str:
    paren_level = 0
    paren_idx_start = None
    for idx, c in enumerate(s):
        if c == '(':
            if paren_level == 0:
                paren_idx_start = idx
            paren_level += 1
        elif c == ')':
            paren_level -= 1
            if paren_level == 0:
                substr = s[:paren_idx_start] + parse_calcstr_ltor(s[paren_idx_start+1:idx]) + s[idx+1:]
                return parse_calcstr_ltor(substr)

    # if here, didn't find a paren group
    symbols = s.split()
    if len(symbols) == 1:
        return symbols[0]
    elif symbols[1] == '+':
        return parse_calcstr_ltor(str(int(symbols[0]) + int(symbols[2].rstrip(')'))) + ' ' + ' '.join(symbols[3:]))
    elif symbols[1] == '*':
        return parse_calcstr_ltor(str(int(symbols[0]) * int(symbols[2].rstrip(')'))) + ' ' + ' '.join(symbols[3:]))


class SymbolList(object):
    def __init__(self, s):
        s = s.rstrip('\n')
        self.input_str = s
        self.value = None
        self.tokens = []    # type: List[SymbolList]

        if s.startswith('('):
            paren_level = 0
            for idx, elt in enumerate(s):
                if elt == '(':
                    paren_level += 1
                elif elt == ')':
                    paren_level -= 1
                    if paren_level == 0:
                        s = s[1:-1] if idx == len(s) - 1 else s
                        break

        paren_level = 0
        paren_start_idx = 0
        elts = s.split()
        if len(elts) == 1:
            self.value = elts[0]
        else:
            for idx, elt in enumerate(elts):
                if elt.startswith('('):
                    if elt.endswith(')'):
                        self.tokens.append(elt.strip('()'))
                        continue
                    if paren_level == 0:
                        paren_start_idx = idx
                    paren_level += elt.count('(')

                elif elt.endswith(')'):
                    paren_level -= elt.count(')')
                    if paren_level == 0:
                        self.tokens.append(SymbolList(' '.join(elts[paren_start_idx:idx+1])))

                elif paren_level == 0:
                    self.tokens.append(SymbolList(elt))

    def __str__(self):
        return str(self.tokens)

    def __repr__(self):
        return str(self.tokens)

    def parse_am(self):
        flattened_tokens = []
        for token in self.tokens:
            flattened_tokens.append(token.value if token.value is not None else token.parse_am())

        # inefficient but i'm bored
        try:
            while True:
                idx = flattened_tokens.index('+')
                flattened_tokens = flattened_tokens[:idx-1] \
                    + [str(int(flattened_tokens[idx-1]) + int(flattened_tokens[idx+1]))] \
                    + flattened_tokens[idx+2:]
        except ValueError:
            pass
        except IndexError:
            print(flattened_tokens)
            raise

        try:
            while True:
                idx = flattened_tokens.index('*')
                flattened_tokens = flattened_tokens[:idx-1] \
                    + [str(int(flattened_tokens[idx-1]) * int(flattened_tokens[idx+1]))] \
                    + flattened_tokens[idx+2:]
        except ValueError:
            pass
        except IndexError:
            print(flattened_tokens)
            raise

        try:
            assert len(flattened_tokens) == 1
        except AssertionError:
            print('Flattening failure:', self.input_str)

        return int(flattened_tokens[0])


def parse_calcstr_am(s: str) -> int:
    symbols = SymbolList(s)
    parsed = symbols.parse_am()
    return parsed


def get_test_input() -> str:
    return textwrap.dedent("""\
    1 + (2 * 3) + (4 * (5 + 6))
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""")


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
        data.append(line)
    return data


def part_1(data):
    ans = sum(int(parse_calcstr_ltor(line)) for line in data)
    print('Part 1:', ans)


def part_2(data):
    ans = sum(parse_calcstr_am(line) for line in data)
    print('Part 2:', ans)


def main():
    data = read_input(day_number=18, test=False)
    part_1(data)
    part_2(data)


class TestParser(unittest.TestCase):
    def test_parse_ltor(self):
        self.assertEqual(parse_calcstr_ltor('1 + (2 * 3) + (4 * (5 + 6))'), '51')
        self.assertEqual(parse_calcstr_ltor('2 * 3 + (4 * 5)'), '26')
        self.assertEqual(parse_calcstr_ltor('5 + (8 * 3 + 9 + 3 * 4 * 3)'), '437')
        self.assertEqual(parse_calcstr_ltor('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), '12240')
        self.assertEqual(parse_calcstr_ltor('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2)'), '13632')

    def test_parse_am(self):
        self.assertEqual(parse_calcstr_am('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(parse_calcstr_am('2 * 3 + (4 * 5)'), 46)
        self.assertEqual(parse_calcstr_am('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 1445)
        self.assertEqual(parse_calcstr_am('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 669060)
        self.assertEqual(parse_calcstr_am('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 23340)
        self.assertEqual(parse_calcstr_am('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + (4 * 2)'), 11674)


if __name__ == "__main__":
    # unittest.main()
    main()
