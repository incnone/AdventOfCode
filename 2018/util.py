import itertools
import operator as op
from functools import reduce
import unittest


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks

    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """

    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


def add_pair(p, q):
    return p[0] + q[0], p[1] + q[1]


def extended_euclid_gcd(a, b):
    """
    Copied from rookieslab

    Returns a list `result` of size 3 where:
    Referring to the equation ax + by = gcd(a, b)
        result[0] is gcd(a, b)
        result[1] is x
        result[2] is y
    """
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r//r
        # This is a pythonic way to swap numbers
        # See the same part in C++ implementation below to know more
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    return [old_r, old_s, old_t]


def solve_crt(congs, mods):
    """Finds the smallest positive x such that x is congruent to congs[i] modulo mods[i] for all i, assuming one
    exists."""
    if len(congs) == 1:
        return congs[0]

    g, m0, m1 = extended_euclid_gcd(mods[0], mods[1])
    n = mods[0]*mods[1]
    x = (congs[1]*m0*mods[0] + congs[0]*m1*mods[1]) % n
    return solve_crt((x,) + congs[2:], (n,) + mods[2:])


def is_prime(n):
    # Not super speedy but ok
    if n < 2:
        return False
    for x in range(2, int(n**0.5) + 1):
        if n % x == 0:
            return False
    return True


class TestGCD(unittest.TestCase):
    def test_eegcd(self):
        for a, b, d in [(24, 18, 6), (54, 36, 18), (120, 428860, 20), (95642, 1681, 1)]:
            g, x, y = extended_euclid_gcd(a, b)
            self.assertEqual(g, d)
            self.assertEqual(x*a + y*b, d)

    def test_crt(self):
        tests = [
            [(1, 2, 3), (2, 3, 5), 23],
            [(1, 2, 3), (3, 5, 7), 52],
        ]
        for congs, mods, crt in tests:
            self.assertEqual(solve_crt(congs, mods), crt)


if __name__ == "__main__":
    unittest.main()
