from getinput import get_input
import itertools


def parse_input(big_str):
    dists = dict()
    cities = set()
    for line in big_str.splitlines(keepends=False):
        items = line.split()
        dists[(items[0], items[2])] = dists[(items[2], items[0])] = int(items[4])
        cities.add(items[0])
        cities.add(items[2])
    return cities, dists


def length(route, dists):
    return sum(dists[r, s] for r, s in zip(route, route[1:]))


def part_1(cities, dists):
    best_dist = 9999999999
    for perm in itertools.permutations(cities):
        best_dist = min(best_dist, length(perm, dists))
    return best_dist


def part_2(cities, dists):
    best_dist = 0
    for perm in itertools.permutations(cities):
        best_dist = max(best_dist, length(perm, dists))
    return best_dist


if __name__ == "__main__":
    cities, dists = parse_input(get_input(day=9))

    print('Part 1:', part_1(cities, dists))
    print('Part 2:', part_2(cities, dists))
