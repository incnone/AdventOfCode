from getinput import get_input
import math
import itertools
import operator


def divisor_sum(n):
    return sum(d for d in range(1, n+1) if n % d == 0)


def divisor_sum_sp(n):
    return sum(d for d in range(1, n+1) if n % d == 0 and n / d <= 50)


def divisor_sum_p(prime_powers):
    """prime_powers should have the form [(p_i, a_i)], and we are finding the divisor sum of the product of p_i**a_i"""
    prod = 1
    for prime, power in prime_powers:
        prod *= (prime**(power+1) - 1) // (prime - 1)
    return prod


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
    """Elves deliver 1 present per house to their first 50 multiples. Find the first house that receives at least
    present_lb presents."""
    present_lb = -(-int(inputstr) // 11)    # ceil(i/11).

    # Handwavy primes/bounds; these depend on the particular input.
    # Not sure how to get a good list here algorithmically at the moment
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    pwr_bds = [16, 6, 4, 3, 3, 2, 2, 2, 2]

    prods = []
    for prs in itertools.product(*list(map(range, pwr_bds))):
        prod = 1
        for p, pwr in zip(primes, prs):
            prod *= p**pwr
        prods.append(prod)

    prods = sorted(prods)
    for prod in prods:
        if divisor_sum_sp(prod) >= present_lb:
            return prod

    return None


if __name__ == "__main__":
    the_input_str = get_input(20)

    # print('Part 1:', part_1(the_input_str))
    print('Part 2:', part_2(the_input_str))
