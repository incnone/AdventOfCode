from defaultlist import defaultlist
import itertools


class TwoSidedTape(object):
    def __init__(self):
        self.right_tape = defaultlist(lambda: 0)    # includes 0
        self.left_tape = defaultlist(lambda: 0)     # starts at -1

    def __getitem__(self, item):
        if item >= 0:
            return self.right_tape[item]
        else:
            return self.left_tape[-item-1]

    def __setitem__(self, key, value):
        if key >= 0:
            self.right_tape[key] = value
        else:
            self.left_tape[-key-1] = value

    def __str__(self):
        return ''.join(str(x) for x in itertools.chain(reversed(self.left_tape), '|', self.right_tape))

    def __repr__(self):
        return ''.join(str(x) for x in itertools.chain(reversed(self.left_tape), '|', self.right_tape))

    def __iter__(self):
        return itertools.chain(reversed(self.left_tape), self.right_tape)

    def bounds(self):
        left_vals = [idx for idx, val in enumerate(self.left_tape) if val]
        right_vals = [idx for idx, val in enumerate(self.right_tape) if val]
        left = -max(left_vals)-1 if left_vals else min(right_vals) if right_vals else 0
        right = max(right_vals)+1 if right_vals else -min(left_vals)-1 if left_vals else 0
        return left, right
