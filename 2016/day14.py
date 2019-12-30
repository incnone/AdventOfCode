from getinput import get_input
import hashlib


class KeyFinder(object):
    @staticmethod
    def _tripled_val(s):
        for c1, c2, c3 in zip(s, s[1:], s[2:]):
            if c1 == c2 == c3:
                return c1
        return None

    @staticmethod
    def _all_quintuples(s):
        quints = []
        for c1, c2, c3, c4, c5 in zip(s, s[1:], s[2:], s[3:], s[4:]):
            if c1 == c2 == c3 == c4 == c5:
                quints.append(c1)
        return quints

    @staticmethod
    def get_hash(salt, idx, stretches=0):
        hash_str = salt + str(idx)
        for _ in range(stretches+1):
            hash_str = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
        return hash_str

    def __init__(self, salt, stretches=0):
        self.salt = salt
        self.idx = 0
        self.hash_cache = []
        self.quintuples = []
        self.stretches = stretches
        for jdx in range(1001):
            s = self.get_hash(self.salt, jdx, self.stretches)
            self.hash_cache.append(s)
            self.quintuples.append(self._all_quintuples(s))

    def is_key(self):
        hashed_val = self.hash_cache[self.idx % 1001]
        tval = self._tripled_val(hashed_val)
        if tval is not None:
            for jdx in range(1001):
                if tval in self.quintuples[jdx] and jdx != (self.idx % 1001):
                    return True
        return False

    def increment(self):
        s = self.get_hash(self.salt, self.idx + 1001, self.stretches)
        self.hash_cache[self.idx % 1001] = s
        self.quintuples[self.idx % 1001] = self._all_quintuples(s)
        self.idx += 1

    def next_key_index(self):
        self.increment()
        while not self.is_key():
            self.increment()
        return self.idx


def part_1(salt):
    key_finder = KeyFinder(salt=salt)
    key_index = None
    for _ in range(64):
        key_index = key_finder.next_key_index()
    return key_index


def part_2(salt):
    key_finder = KeyFinder(salt=salt, stretches=2016)
    key_index = None
    for _ in range(64):
        key_index = key_finder.next_key_index()
    return key_index


if __name__ == "__main__":
    the_big_str = get_input(14)

    # print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
