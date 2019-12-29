from getinput import get_input
import itertools
import copy


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

    # p[i][j] = There exists a subset of the first j weights summing to i (hence, we want to know p[k][n])
    p = [[False for _ in range(n + 1)] for _ in range(k + 1)]
    for j in range(len(p[0])):
        p[0][j] = True

    # Fill out one row at a time
    for i in range(1, k + 1):
        for j in range(1, n + 1):
            # If the next weight isn't too large, then we can make i either by using this weight and prior weights,
            # or by only using prior weights
            if (i - weights[j-1]) >= 0:
                p[i][j] = p[i][j-1] or p[i - weights[j-1]][j-1]
            # Otherwise, the only way to make a weight of i is with the weights before this one
            else:
                p[i][j] = p[i][j-1]

    return p[k][n]


def balanceable(subset, weights):
    remaining_weights = [w for w in weights if w not in subset]
    desired_weight = sum(subset)
    if sum(remaining_weights) != 2*desired_weight:
        return False
    return partitionable(weights)


def sums_exist_hlpr(weights, idx, sums, cache):
    """Check whether the set weights[:idx+1] can be split into sets with the sums given in sums. Use cache
    to store the result of computations."""

    if (idx, sums) in cache:
        return cache[(idx, sums)]
    if not any(x != 0 for x in sums):
        return True
    if idx < 0:
        return False

    sums_exist = False
    for jdx in range(len(sums)):
        remainder = sums[jdx] - weights[idx]
        if remainder >= 0:
            sums_exist = sums_exist \
                         or sums_exist_hlpr(weights, idx-1, sums[:jdx] + (remainder,) + sums[jdx+1:], cache)

    cache[(idx, sums)] = sums_exist
    return sums_exist


def tripartitionable(weights):
    wsum = sum(weights)
    if wsum % 3 != 0:
        return False

    n = len(weights)
    cache = dict()
    answer = sums_exist_hlpr(weights, n-1, (wsum//3, wsum//3, wsum//3), cache)
    return answer


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
    packagesum = sum(weights)
    assert packagesum % 4 == 0
    for subset_size in range(1, len(weights)+1):
        subsets = sorted(itertools.combinations(weights, subset_size), key=lambda x: list_prod(x))
        for subset in subsets:
            if sum(subset) != packagesum // 4:
                continue
            if tripartitionable([w for w in weights if w not in subset]):
                return list_prod(subset)
    return None


if __name__ == "__main__":
    the_pkg_weights = parse_input(get_input(24))

    print('Part 1:', part_1(the_pkg_weights))
    print('Part 2:', part_2(the_pkg_weights))
