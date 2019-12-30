from getinput import get_input
from util import add_pair
import itertools


class Maze(object):
    def __init__(self, number):
        self.number = number
        self.cache = dict()

    def walkable(self, x, y):
        if x < 0 or y < 0:
            return False
        if (x, y) in self.cache:
            return self.cache[(x, y)]
        z = '{:b}'.format(x*x + 3*x + 2*x*y + y + y*y + self.number)
        return not bool(z.count('1') % 2)


def part_1(n):
    orthos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    maze = Maze(n)
    distances = {}
    to_check = [((1, 1), 0)]
    wanted = (31, 39)
    while wanted not in distances:
        next_to_check, dist = to_check.pop(0)
        distances[next_to_check] = dist
        for p in orthos:
            q = add_pair(next_to_check, p)
            if q not in distances.keys() and maze.walkable(*q):
                to_check.append((q, dist+1))
    return distances[wanted]


def part_2(n):
    orthos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    maze = Maze(n)
    distances = {}
    to_check_list = [(1, 1)]
    dist = 0
    while dist < 51:
        next_check_list = []
        for next_to_check in to_check_list:
            distances[next_to_check] = dist
            for p in orthos:
                q = add_pair(next_to_check, p)
                if q not in distances.keys() and maze.walkable(*q):
                    next_check_list.append(q)
        to_check_list = next_check_list
        dist += 1

    return sum(1 for x in distances.values() if x <= 50)


if __name__ == "__main__":
    the_input = int(get_input(13))

    print('Part 1:', part_1(the_input))
    print('Part 2:', part_2(the_input))
