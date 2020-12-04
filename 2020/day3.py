import textwrap


class TreeCyl(object):
    def __init__(self, trees: set, width: int, height: int):
        self.trees = trees
        self.width = width
        self.height = height

    def __str__(self):
        retval = ''
        for row in range(self.height):
            for col in range(self.width):
                retval += '#' if (row, col) in self.trees else '.'
            retval += '\n'
        return retval

    def has_tree(self, x: int, y: int):
        return (x % self.width, y) in self.trees


def test_input() -> str:
    return textwrap.dedent("""
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#""")


def read_input(day_num: int):
    trees = set()
    filename = 'input/dec{}.txt'.format(day_num)
    width = 0
    height = 0
    with open(filename, 'r') as file:
        for row, line in enumerate(file):
            width = max(width, len(line.rstrip('\n')))
            height += 1
            for col, char in enumerate(line):
                if char == '#':
                    trees.add((col, row))
    return TreeCyl(trees=trees, width=width, height=height)


def read_test_input():
    trees = set()
    width = 0
    height = 0
    for row, line in enumerate(test_input().splitlines()[1:]):
        width = max(width, len(line.rstrip('\n')))
        height += 1
        for col, char in enumerate(line):
            if char == '#':
                trees.add((col, row))

    return TreeCyl(trees=trees, width=width, height=height)


def num_trees_hit(trees: TreeCyl, movex: int, movey: int):
    x = 0
    y = 0
    num_trees = 0
    while y < trees.height:
        if trees.has_tree(x, y):
            num_trees += 1
        x += movex
        y += movey
    return num_trees


def part_1(trees: TreeCyl):
    print("Part 1: Num trees hit = {}".format(num_trees_hit(trees, 3, 1)))


def part_2(trees):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    prod = 1
    for slope in slopes:
        prod *= num_trees_hit(trees=trees, movex=slope[0], movey=slope[1])
    print("Part 2: Product = {}".format(prod))


def main():
    #data = read_test_input()
    data = read_input(3)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
