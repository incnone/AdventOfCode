from getinput import get_input


def parse_input(s):
    pairs = []
    for line in s.splitlines(keepends=False):
        pairs.append(tuple(int(c) for c in line.split('-')))
    return pairs


class IntervalList(object):
    def __init__(self):
        self.intervals = []     # sorted

    def add(self, mn, mx):
        self._add_i(mn, mx)

    def _add_f(self, mn, mx):
        mindex = None
        maxdex = None
        for idx in range(len(self.intervals)):
            x, y = self.intervals[idx]
            if x <= mn:
                mindex = idx
            if y >= mx and maxdex is None:
                maxdex = idx

        # Remove any intervals contained entirely within the new interval
        if mindex is not None and self.intervals[mindex][1] >= mn:
            mn = self.intervals[mindex][0]
            mindex = mindex - 1

        if maxdex is not None and self.intervals[maxdex][0] <= mx:
            mx = self.intervals[maxdex][1]
            maxdex = maxdex + 1

        start = self.intervals[:mindex+1] if mindex is not None else []
        end = self.intervals[maxdex:] if maxdex is not None else []
        self.intervals = start + [(mn, mx)] + end

    def _add_i(self, mn, mx):
        mindex = None
        maxdex = None
        for idx in range(len(self.intervals)):
            x, y = self.intervals[idx]
            if x <= mn:
                mindex = idx
            if y >= mx and maxdex is None:
                maxdex = idx

        if mindex is not None and self.intervals[mindex][1] >= mn - 1:
            mn = self.intervals[mindex][0]
            mindex = mindex - 1

        if maxdex is not None and self.intervals[maxdex][0] <= mx + 1:
            mx = self.intervals[maxdex][1]
            maxdex = maxdex + 1

        start = self.intervals[:mindex+1] if mindex is not None else []
        end = self.intervals[maxdex:] if maxdex is not None else []
        self.intervals = start + [(mn, mx)] + end


def part_1(big_str):
    pairs = parse_input(big_str)
    ivals = IntervalList()
    for p, q in pairs:
        ivals.add(p, q)
    return ivals.intervals[0][1] + 1


def part_2(big_str):
    pairs = parse_input(big_str)
    ivals = IntervalList()
    for p, q in pairs:
        ivals.add(p, q)

    total = 4294967296
    for p, q in ivals.intervals:
        total -= (q - p) + 1
    return total


if __name__ == "__main__":
    the_big_str = get_input(20)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
