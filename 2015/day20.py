from getinput import get_input
import math
import itertools
import operator


def divisor_sum(n):
    return sum(d for d in range(1, n+1) if n % d == 0)


def part_1(inputstr):
    divisor_sum_lb = int(inputstr) // 10

    # Handwavy primes/bounds; these depend on the particular input.
    # Not sure how to get a good list here algorithmically at the moment
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    pwr_bds = [21, 9, 5, 4, 4, 1, 1, 1]

    prods = []
    for prs in itertools.product(*list(map(range, pwr_bds))):
        prod = 1
        for p, pwr in zip(primes, prs):
            prod *= p**pwr
        prods.append(prod)

    prods = sorted(prods)
    for prod in prods:
        if divisor_sum(prod) >= divisor_sum_lb:
            return prod

    return None


def part_2(inputstr):
    for x in range(1, 51):
        print(x, divisor_sum(x))


if __name__ == "__main__":
    the_input_str = get_input(20)

    # print('Part 1:', part_1(the_input_str))
    print('Part 2:', part_2(the_input_str))
