from getinput import get_input
import itertools
import textwrap
from grid import Loc2, Loc2Grid
from util import int2base


class WoodedArea(object):
    @staticmethod
    def _arr_from_ternary(n, width, height):
        nstr = int2base(n, 3)
        arr = []
        for y in range(height):
            line = []
            for x in range(width):
                if x + y*width < len(nstr):
                    c = nstr[-(x+y*width+1)]
                    line.append('#' if c == '2' else '|' if c == '1' else '.')
                else:
                    line.append('.')
            arr.append(line)
        return arr

    def __init__(self, grid):
        self.grid = grid

    @property
    def ternary_rep(self):
        ternary_str = ''.join(
            ''.join('2' if c == '#' else '1' if c == '|' else '0' for c in line)
            for line in self.grid.arr
        )
        return int(ternary_str, 3)

    @property
    def width(self):
        return len(self.grid.arr[0])

    @property
    def height(self):
        return len(self.grid.arr)

    def __str__(self):
        return '\n'.join(
            ''.join(c for c in line)
            for line in self.grid.arr
        )

    @property
    def trees(self):
        return sum(sum(1 if q == '|' else 0 for q in line) for line in self.grid.arr)

    @property
    def lumberyards(self):
        return sum(sum(1 if q == '#' else 0 for q in line) for line in self.grid.arr)

    def run_for_minutes(self, n):
        self.power(n+1)

    def power(self, n):
        if n == 0:
            return self

        ternary_to_idx = {self.ternary_rep: 1}
        idx_to_ternary = {1: self.ternary_rep}
        for idx in range(2, n+1):
            # if idx % 100 == 0:
            #     print(idx)

            self.update()

            if self.ternary_rep in ternary_to_idx:
                first_idx = ternary_to_idx[self.ternary_rep]
                # print('Repetition: a^{} = a^{}'.format(idx, first_idx))
                cycle_length = idx - first_idx
                remainder = (n - first_idx) % cycle_length
                if (first_idx + remainder) in idx_to_ternary:
                    tern = idx_to_ternary[first_idx+remainder]
                    self.grid = Loc2Grid(self._arr_from_ternary(tern, self.width, self.height))
                    return self
                else:
                    last_idx, last_area = max(idx_to_ternary.items(), key=lambda q: q[0])
                    self.grid = Loc2Grid(self._arr_from_ternary(last_area, self.width, self.height))
                    for _ in range(last_idx - first_idx, remainder):
                        self.update()
                    return self
            else:
                tern_rep = self.ternary_rep
                ternary_to_idx[tern_rep] = idx
                idx_to_ternary[idx] = tern_rep
        return self

    def update(self):
        new_grid = Loc2Grid(list(list(x for x in line) for line in self.grid.arr))
        for x, y in itertools.product(range(self.width), range(self.height)):
            loc = Loc2(x, y)
            contents = self.grid[loc]

            # Open area
            if contents == '.':
                trees = sum(1 if self.grid[q] == '|' else 0 for q in Loc2.adj_sup(loc) if q in self.grid)
                if trees >= 3:
                    new_grid[loc] = '|'

            # Trees
            elif contents == '|':
                lumberyards = sum(1 if q in self.grid and self.grid[q] == '#' else 0 for q in Loc2.adj_sup(loc))
                if lumberyards >= 3:
                    new_grid[loc] = '#'

            # Lumberyards
            elif contents == '#':
                tree = any(q in self.grid and self.grid[q] == '|' for q in Loc2.adj_sup(loc))
                lumberyard = any(q in self.grid and self.grid[q] == '#' for q in Loc2.adj_sup(loc))
                if not (tree and lumberyard):
                    new_grid[loc] = '.'
        self.grid = new_grid
        return self


def parse_input(s: str):
    arr = list(list(c for c in line) for line in s.splitlines(keepends=False))
    return WoodedArea(Loc2Grid(arr))


def part_1(input_str: str):
    # input_str = test_input()
    wooded_area = parse_input(input_str)
    wooded_area.run_for_minutes(10)
    return wooded_area.trees*wooded_area.lumberyards


def part_2(input_str: str):
    # input_str = test_input()
    wooded_area = parse_input(input_str)
    wooded_area.run_for_minutes(1000000000)

    return wooded_area.trees*wooded_area.lumberyards


def test_input():
    test_num = 1
    if test_num == 0:
        return textwrap.dedent("""\
        .#.#...|#.
        .....#|##|
        .|..|...#.
        ..|#.....#
        #.#|||#|#|
        ...#.||...
        .|....|...
        ||...#|.#|
        |.||||..|.
        ...#.|..|.""")
    elif test_num == 1:
        return textwrap.dedent("""\
        ||||||||||
        ..........
        ##########
        ||||||||||
        ..........
        ..........
        ..........
        ..........
        ..........
        ..........
        ..........""")


def main():
    input_str = get_input(18)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
