from getinput import get_input
from enum import Enum
import itertools
import operator


def list_prod(x):
    prod = 1
    for s in x:
        prod *= s
    return prod


def partitionable(weights):
    weight_sum = sum(w for w in weights)
    if weight_sum % 2 != 0:
        return False
    n = len(weights)
    k = weight_sum // 2

    p = [[False for _ in range(n + 1)] for _ in range(k + 1)]
    for j in range(len(p[0])):
        p[0][j] = True

    for i in range(1, k + 1):
        for j in range(1, n + 1):
            if (i - weights[j-1]) >= 0:
                p[i][j] = p[i][j-1] or p[i - weights[j-1]][j-1]
            else:
                p[i][j] = p[i][j-1]

    return p[k][n]


def balanceable(subset, weights):
    remaining_weights = [w for w in weights if w not in subset]
    desired_weight = sum(subset)
    if sum(remaining_weights) != 2*desired_weight:
        return False
    return partitionable(weights)


def parse_input(s):
    weights = []
    for line in s.splitlines(keepends=False):
        weights.append(int(line))
    return weights


def part_1(weights):
    for subset_size in range(1, len(weights)+1):
        subsets = sorted(itertools.combinations(weights, subset_size), key=lambda x: list_prod(x))
        for subset in subsets:
            if balanceable(subset, weights):
                return list_prod(subset)
    return None


def part_2(weights):
    pass


if __name__ == "__main__":
    the_pkg_weights = parse_input(get_input(24))

    # print('Part 1:', part_1(the_pkg_weights))
    print('Part 2:', part_2(the_pkg_weights))
