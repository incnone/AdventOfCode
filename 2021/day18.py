import textwrap
from typing import Union


def get_test_input() -> str:
    return textwrap.dedent("""\
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return data


class SnailfishNumber(object):
    @staticmethod
    def add(n1, n2):
        result = SnailfishNumber(f'[{str(n1)},{str(n2)}]')
        result.reduce()
        return result

    def __init__(self, s: str, cursor=0, parent=None):
        self._cursor = cursor
        self._cursor += 1     # initial [
        self._parent = parent
        self._this_exploded = False
        self.left = None
        self.right = None

        if s[self._cursor] == '[':
            self.left = SnailfishNumber(s, self._cursor, self)
            self._cursor = self.left._cursor
        else:
            self.left = int(s[self._cursor])
            self._cursor += 1
        self._cursor += 1     # comma
        if s[self._cursor] == '[':
            self.right = SnailfishNumber(s, self._cursor, self)
            self._cursor = self.right._cursor
        else:
            self.right = int(s[self._cursor])
            self._cursor += 1
        self._cursor += 1     # final ]

    def __str__(self):
        return f'[{str(self.left)},{str(self.right)}]'

    def reduce(self):
        while True:
            if self._explode(depth=0, depth_max=4):
                continue
            if self._split():
                continue
            break

    def _explode(self, depth, depth_max=4):
        if depth >= 4 and type(self.left) is int and type(self.right) is int:

            # Find left number
            p = self._parent
            c = self
            while p is not None and c != p.right:
                c = p
                p = c._parent
            if p is not None:
                if type(p.left) is int:
                    p.left += self.left
                else:
                    c = p.left
                    while type(c.right) is not int:
                        c = c.right
                    c.right += self.left

            # Find right number
            p = self._parent
            c = self
            while p is not None and c != p.left:
                c = p
                p = c._parent
            if p is not None:
                if type(p.right) is int:
                    p.right += self.right
                else:
                    c = p.right
                    while type(c.left) is not int:
                        c = c.left
                    c.left += self.right

            # Replace with zero
            if self == self._parent.left:
                self._parent.left = 0
            elif self == self._parent.right:
                self._parent.right = 0

            return True

        if type(self.left) is SnailfishNumber:
            left_exploded = self.left._explode(depth+1, depth_max)
            if left_exploded:
                return True

        if type(self.right) is SnailfishNumber:
            right_exploded = self.right._explode(depth+1, depth_max)
            if right_exploded:
                return True

        return False


    def _split(self):
        if type(self.left) is int and self.left >= 10:
            val = self.left
            self.left = SnailfishNumber('[0,0]', parent=self)
            self.left.left = val // 2
            self.left.right = (val + 1)//2
            return True

        if type(self.left) is SnailfishNumber:
            left_split = self.left._split()
            if left_split:
                return True

        if type(self.right) is int and self.right >= 10:
            val = self.right
            self.right = SnailfishNumber('[0,0]', parent=self)
            self.right.left = val // 2
            self.right.right = (val+1)//2
            return True

        if type(self.right) is SnailfishNumber:
            right_split = self.right._split()
            if right_split:
                return True

        return False


    def magnitude(self):
        return 3*(self.left if type(self.left) is int else self.left.magnitude()) \
               + 2*(self.right if type(self.right) is int else self.right.magnitude())


def test_explode():
    cases = [
        #"[[[[[9,8],1],2],3],4]",
        #"[7,[6,[5,[4,[3,2]]]]]",
        #"[[6,[5,[4,[3,2]]]],1]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        #"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    ]

    for s in cases:
        print(s)
        snum = SnailfishNumber(s)
        snum._explode(depth=0)
        print(str(snum))


def test_reduce():
    cases = [
        "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
    ]

    for s in cases:
        print(s)
        snum = SnailfishNumber(s)
        snum.reduce()
        print(str(snum))


def test_magnitude():
    cases = [
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    ]

    for s in cases:
        print(s)
        snum = SnailfishNumber(s)
        snum.reduce()
        print(str(snum.magnitude()))


def part_1(data):
    s = SnailfishNumber(data[0])
    for line in data[1:]:
        s = SnailfishNumber.add(s, SnailfishNumber(line))

    print(s)
    print(f'Part 1: {s.magnitude()}')



def part_2(data):
    nums = list(SnailfishNumber(s) for s in data)
    maxval = 0
    for x in nums:
        for y in nums:
            if x != y:
                maxval = max(maxval, SnailfishNumber.add(x, y).magnitude())

    print(f'Part 2: {maxval}')


def main():
    data = read_input(day_number=18, test=False)

    #test_magnitude()
    #part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
