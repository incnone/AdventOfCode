from getinput import get_input
import textwrap
import unittest


def swap_index(s, idx, jdx):
    mndx = min(idx, jdx)
    mxdx = max(idx, jdx)
    return s[:mndx] + s[mxdx] + s[mndx + 1:mxdx] + s[mndx] + s[mxdx + 1:]


def rotate_string_left(s, r):
    r = r % len(s)
    return s[r:] + s[:r]


def reverse_string(s, x, y):
    return s[:x] + ''.join(reversed(s[x:y+1])) + s[y+1:]


def move_letter(s: str, x, y):
    if x == y:
        return s
    elif x < y:
        return s[:x] + s[x+1:y+1] + s[x] + s[y+1:]
    elif y < x:
        return s[:y] + s[x] + s[y:x] + s[x+1:]


def execute(instr, s: str):
    words = instr.split()
    if words[0] == 'swap':
        if words[1] == 'position':
            return swap_index(s, int(words[2]), int(words[5]))
        elif words[1] == 'letter':
            return swap_index(s, s.index(words[2]), s.index(words[5]))
    elif words[0] == 'rotate':
        if words[1] == 'left':
            return rotate_string_left(s, int(words[2]))
        elif words[1] == 'right':
            return rotate_string_left(s, -int(words[2]))
        elif words[1] == 'based':
            idx = s.index(words[-1])
            rotations = idx + 1 + (1 if idx >= 4 else 0)
            return rotate_string_left(s, -rotations)
    elif words[0] == 'reverse':
        return reverse_string(s, int(words[2]), int(words[4]))
    elif words[0] == 'move':
        return move_letter(s, int(words[2]), int(words[5]))


def unexecute(instr, s: str):
    backrotate_map = {
        1: 1,
        3: 2,
        5: 3,
        7: 4,
        2: 6,
        4: 7,
        6: 0,
        0: 1
    }

    words = instr.split()
    if words[0] == 'swap':
        if words[1] == 'position':
            return swap_index(s, int(words[2]), int(words[5]))
        elif words[1] == 'letter':
            return swap_index(s, s.index(words[2]), s.index(words[5]))
    elif words[0] == 'rotate':
        if words[1] == 'left':
            return rotate_string_left(s, -int(words[2]))
        elif words[1] == 'right':
            return rotate_string_left(s, int(words[2]))
        elif words[1] == 'based':
            idx = s.index(words[-1])
            rotations = backrotate_map[idx]
            return rotate_string_left(s, rotations)
    elif words[0] == 'reverse':
        return reverse_string(s, int(words[2]), int(words[4]))
    elif words[0] == 'move':
        return move_letter(s, int(words[5]), int(words[2]))


def part_1(big_str):
    start_str = 'abcdefgh'
    for line in big_str.splitlines(keepends=False):
        start_str = execute(line, start_str)
    return start_str


def part_2(big_str):
    end_str = 'fbgdceah'
    for line in reversed(big_str.splitlines(keepends=False)):
        end_str = unexecute(line, end_str)
    return end_str


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.instrs = textwrap.dedent("""\
        swap position 4 with position 0
        swap letter d with letter b
        reverse positions 0 through 4
        rotate left 1 step
        move position 1 to position 4
        move position 3 to position 0
        rotate based on position of letter b
        rotate based on position of letter d""")
        self.desired = [
            'abcdefgh',
            'ebcdafgh',
            'edcbafgh',
            'abcdefgh',
            'bcdefgha',
            'bdefcgha',
            'fbdecgha',
            'hafbdecg',
            'fbdecgha'
        ]

    def test_fwd(self):
        s = self.desired[0]
        for i, d in zip(self.instrs.splitlines(keepends=False), self.desired[1:]):
            s = execute(i, s)
            self.assertEqual(d, s, msg=i)

    def test_bkwd(self):
        s = self.desired[-1]
        for i, d in zip(self.instrs.splitlines(keepends=False)[::-1], self.desired[-2::-1]):
            s = unexecute(i, s)
            self.assertEqual(d, s, msg=i)


if __name__ == "__main__":
    # unittest.main()

    the_big_str = get_input(21)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
