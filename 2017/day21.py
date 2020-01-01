from getinput import get_input
import itertools
import textwrap


class FractalImage(object):
    @staticmethod
    def full_rules(rules):
        full_rules = dict()
        for key, val in rules.items():
            for k in FractalImage.all_flips_and_rotations(key):
                full_rules[k] = val
        return full_rules

    @staticmethod
    def grid_str(t):
        return '\n'.join(''.join('#' if c else '.' for c in line) for line in t)

    @staticmethod
    def rotate_right(t):
        return tuple(tuple(t[i][j] for i in range(len(t) - 1, -1, -1)) for j in range(len(t[0])))

    @staticmethod
    def flip_horiz(t):
        return tuple(tuple(t[j][i] for i in range(len(t[0]) - 1, -1, -1)) for j in range(len(t)))

    @staticmethod
    def all_flips_and_rotations(t):
        """t is a """
        all_of_em = [t]
        for _ in range(3):
            all_of_em.append(FractalImage.rotate_right(all_of_em[-1]))
        for x in range(4):
            all_of_em.append(FractalImage.flip_horiz(all_of_em[x]))
        return set(all_of_em)

    def __init__(self, rules):
        self.image = start_pattern()
        self.rules = self.full_rules(rules)

    def __str__(self):
        return FractalImage.grid_str(self.image)

    def subpattern(self, x, y, w, h):
        return tuple(tuple(self.image[j][i] for i in range(x, x+w)) for j in range(y, y+h))

    def next_pattern(self):
        n = len(self.image)
        next_pattern = []

        # If even size, break into 2x2 blocks; otherwise, break into 3x3 blocks
        if n % 2 == 0:
            block_size = 2
        else:
            block_size = 3

        # Construct the next image
        for y in range(n // block_size):
            rows = [tuple()]*(block_size+1)
            for x in range(n // block_size):
                rep_pattern = self.rules[self.subpattern(block_size*x, block_size*y, block_size, block_size)]
                for idx in range(len(rows)):
                    rows[idx] += rep_pattern[idx]
            next_pattern += rows
        self.image = tuple(next_pattern)

    def num_on(self):
        return sum(sum(1 if c else 0 for c in line) for line in self.image)


def parse_to_grid(s):
    return tuple(tuple(True if c == '#' else False for c in line) for line in s.split('/'))


def parse_input(s):
    rules = dict()
    for line in s.splitlines(keepends=False):
        words = line.split(' => ')
        rules[parse_to_grid(words[0])] = parse_to_grid(words[1])
    return rules


def start_pattern():
    s = textwrap.dedent("""\
    .#.
    ..#
    ###""")
    return tuple(tuple(True if c == '#' else False for c in line) for line in s.splitlines(keepends=False))


def test_input():
    return textwrap.dedent("""\
    ../.# => ##./#../...
    .#./..#/### => #..#/..../..../#..#""")


def part_1(input_str):
    rules = parse_input(input_str)
    image = FractalImage(rules=rules)
    for i in range(5):
        image.next_pattern()
    return image.num_on()


def part_2(input_str):
    rules = parse_input(input_str)
    image = FractalImage(rules=rules)
    for i in range(18):
        image.next_pattern()
    return image.num_on()


def main():
    input_str = get_input(21)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
