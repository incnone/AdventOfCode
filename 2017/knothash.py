from getinput import get_input
import itertools
from util import grouper


class Ring(object):
    def __init__(self, length):
        self.numbers = list(range(length))
        self.start = 0

    def __len__(self):
        return len(self.numbers)

    def __str__(self):
        return 'R' + str(self.numbers[self.start:] + self.numbers[:self.start])

    def __repr__(self):
        return 'R[{}]'.format(self.start) + str(self.numbers)

    def __getitem__(self, item):
        return self.numbers[(item + self.start) % len(self)]

    def __iter__(self):
        return itertools.islice(itertools.cycle(self.numbers), self.start, self.start + len(self))

    @staticmethod
    def knot_twist(ring, start, length):
        if not 0 <= length <= len(ring):
            raise RuntimeError('Bad knot twist')

        start = (start + ring.start) % len(ring)
        stop = start + length
        backwards_stop = -stop % len(ring)

        new_ring = Ring(0)
        new_ring.numbers = list(itertools.chain(
            itertools.islice(itertools.cycle(reversed(ring.numbers)), backwards_stop, backwards_stop + length),
            itertools.islice(itertools.cycle(ring.numbers), stop, start+len(ring))
        ))
        new_ring.start = (ring.start - start) % len(ring)
        return new_ring


def sparse_knot_hash(lengths, string_length, rounds=1):
    numbers = Ring(string_length)
    cursor = 0
    skip_size = 0
    for _ in range(rounds):
        for ln in lengths:
            numbers = Ring.knot_twist(numbers, cursor, ln)
            cursor = (cursor + ln + skip_size) % string_length
            skip_size += 1
    return numbers


def knot_hash(s):
    twist_lengths = [ord(x) for x in s] + [17, 31, 73, 47, 23]
    sparse_hash = sparse_knot_hash(twist_lengths, 256, rounds=64)
    dense_hash = ''
    for x in grouper(sparse_hash, 16):
        val = x[0]
        for k in x[1:]:
            val ^= k
        dense_hash += '{:0>2}'.format(hex(val)[2:])
    return dense_hash
