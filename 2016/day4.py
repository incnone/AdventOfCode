from getinput import get_input
from util import grouper
from collections import Counter
import textwrap


class Room(object):
    def __init__(self, s):
        self.checksum = s[-6:-1]
        self.sector_id = int(s[-10:-7])
        self.room_name = s[:-11]

    def __str__(self):
        return '{}-{}[{}]'.format(self.room_name, self.sector_id, self.checksum)

    def valid(self):
        c = Counter(self.room_name)
        letters = list(sorted(
            [x for x in c.keys() if x != '-'],
            key=lambda x: (-c[x], x),
        ))
        return self.checksum == ''.join(letters[:5])

    def decrypted_name(self):
        s = ''
        for c in self.room_name:
            if c == '-':
                s += ' '
            else:
                s += chr(ord('a') + (((ord(c) - ord('a')) + self.sector_id) % 26))
        return s


def parse_input(s):
    rooms = []
    for line in s.splitlines(keepends=False):
        rooms.append(Room(line))
    return rooms


def part_1(rooms):
    return sum(r.sector_id for r in rooms if r.valid())


def part_2(rooms):
    for r in rooms:
        if 'northpole' in r.decrypted_name():
            return r.sector_id


def test_input():
    testrooms = textwrap.dedent("""\
    aaaaa-bbb-z-y-x-123[abxyz]
    a-b-c-d-e-f-g-h-987[abcde]
    not-a-real-room-404[oarel]
    totally-real-room-200[decoy]
    qzmt-zixmtkozy-ivhz-343[blahe]""")
    return parse_input(testrooms)


if __name__ == "__main__":
    the_rooms = parse_input(get_input(4))

    print('Part 1:', part_1(the_rooms))
    print('Part 2:', part_2(the_rooms))
