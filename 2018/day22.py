from getinput import get_input
import itertools
import textwrap
from grid import Loc2, Loc2Grid
from enum import Enum
from priorityqueue import PriorityQueue
from typing import List, Tuple


class CaveItem(Enum):
    NOTHING = 0
    TORCH = 1
    CLIMBING = 2


class RegionType(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2
    WALL = 100

    @property
    def char(self):
        chars = {
            RegionType.ROCKY: '.',
            RegionType.WET: '=',
            RegionType.NARROW: '|'
        }
        return chars[self]


class Cave(object):
    top_x_fac = 16807
    left_y_fac = 48271
    base = 20183

    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.el = self.init_erosion_levels()
        self.xmax = target.x
        self.ymax = target.y

    def __getitem__(self, loc):
        try:
            if loc.x < 0 or loc.y < 0:
                return RegionType.WALL

            if loc.x > self.xmax:
                for x in range(self.xmax+1, loc.x+1):
                    self.el[0].append(self.er_lev(Cave.top_x_fac * x))
                for y in range(1, self.ymax+1):
                    for x in range(self.xmax+1, loc.x+1):
                        self.el[y].append(self.er_lev(self.el[y-1][x]*self.el[y][x-1]))
            self.xmax = max(self.xmax, loc.x)
            if loc.y > self.ymax:
                for y in range(self.ymax+1, loc.y+1):
                    new_row = [self.er_lev(Cave.left_y_fac * y)]
                    for x in range(1, self.xmax+1):
                        new_row.append(self.er_lev(self.el[y-1][x] * new_row[-1]))
                    self.el.append(new_row)
            self.ymax = max(self.ymax, loc.y)
            return RegionType(self.el[loc.y][loc.x] % 3)
        except IndexError:
            print(loc)
            print(self)
            raise

    def __str__(self):
        return '\n'.join(''.join(RegionType(r % 3).char for r in row) for row in self.el)

    def er_lev(self, g):
        return (g + self.depth) % Cave.base

    def init_erosion_levels(self):
        erosion_level = [list(self.er_lev(Cave.top_x_fac * x) for x in range(self.target.x + 1))]
        for y in range(1, self.target.y + 1):
            cave_row = [self.er_lev(Cave.left_y_fac * y)]
            for x in range(1, self.target.x + 1):
                if Loc2(x, y) == self.target:
                    cave_row.append(self.er_lev(0))
                else:
                    cave_row.append(self.er_lev(erosion_level[-1][x] * cave_row[-1]))
            erosion_level.append(cave_row)
        return erosion_level

    def get_neighbors(self, loc, cave_item) -> List[Tuple[Tuple[Loc2, CaveItem], int]]:
        # return a list of ((loc, item), distance)
        neighbors = []
        for q in Loc2.adj_L1(loc):
            if self[q].value not in [RegionType.WALL.value, cave_item.value]:  # traversable with this item
                neighbors.append(((q, cave_item), 1))
        for item in CaveItem:
            if item != cave_item and item.value != self[loc].value:
                neighbors.append(((loc, item), 7))
        return neighbors


def parse_input(s: str):
    lines = s.splitlines(keepends=False)
    depth = int(lines[0].split()[-1])
    line2wds = lines[1].split()
    target = tuple(int(x) for x in line2wds[-1].split(','))

    return depth, Loc2(*target)


def part_1(input_str: str):
    # input_str = test_input()
    depth, target = parse_input(input_str)
    cave = get_cave_array(depth, target)

    return sum(cave[Loc2(x, y)].value for x, y in itertools.product(range(target.x + 1), range(target.y + 1)))


def part_2(input_str: str):
    # Extremely slow even with the fake x < 200 optimization. Maybe should look into A* for this one

    # input_str = test_input()
    depth, target = parse_input(input_str)
    cave = Cave(depth=depth, target=target)
    start = (Loc2(0, 0), CaveItem.TORCH)
    end = (target, CaveItem.TORCH)

    # Djikstra's algorithm.
    pq = PriorityQueue()
    pq.add_task(start, priority=0)
    last_distance = 0
    while pq:
        distance, next_node = pq.pop_task_with_priority()
        if distance != last_distance:
            print(distance)
            last_distance = distance
        if next_node == end:
            return distance
        for neighbor, neighbor_dist in cave.get_neighbors(next_node[0], next_node[1]):
            if neighbor[0].x >= 200:  # Pray that going that far over is bad
                continue
            pq.add_task_if_better(neighbor, priority=distance+neighbor_dist)


def test_input():
    return textwrap.dedent("""\
    depth: 510
    target: 10,10""")


def main():
    input_str = get_input(22)
    # print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
