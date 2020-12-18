import textwrap
from enum import Enum


class Instruction(object):
    def __init__(self, s: str):
        self.type = s[0]
        self.val = int(s[1:])


class Ship(object):
    def __init__(self):
        self.dir = (1, 0)
        self.loc = (0, 0)
        self.waypoint = (10, -1)

    def follow_1(self, i: Instruction):
        if i.type == 'N':
            self.loc = (self.loc[0], self.loc[1] - i.val)
        elif i.type == 'S':
            self.loc = (self.loc[0], self.loc[1] + i.val)
        elif i.type == 'E':
            self.loc = (self.loc[0] + i.val, self.loc[1])
        elif i.type == 'W':
            self.loc = (self.loc[0] - i.val, self.loc[1])
        elif i.type == 'L':
            self.do_turn(i.val)
        elif i.type == 'R':
            self.do_turn(-i.val)
        elif i.type == 'F':
            self.loc = (self.loc[0] + i.val*self.dir[0], self.loc[1] + i.val*self.dir[1])

    def follow_2(self, i: Instruction):
        if i.type == 'N':
            self.waypoint = (self.waypoint[0], self.waypoint[1] - i.val)
        elif i.type == 'S':
            self.waypoint = (self.waypoint[0], self.waypoint[1] + i.val)
        elif i.type == 'E':
            self.waypoint = (self.waypoint[0] + i.val, self.waypoint[1])
        elif i.type == 'W':
            self.waypoint = (self.waypoint[0] - i.val, self.waypoint[1])
        elif i.type == 'L':
            self.do_waypoint_turn(i.val)
        elif i.type == 'R':
            self.do_waypoint_turn(-i.val)
        elif i.type == 'F':
            self.loc = (self.loc[0] + i.val*self.waypoint[0], self.loc[1] + i.val*self.waypoint[1])

    def do_turn(self, deg: int):
        if deg % 360 == 90:
            self.dir = (self.dir[1], -self.dir[0])
        elif deg % 360 == 180:
            self.dir = (-self.dir[0], -self.dir[1])
        elif deg % 360 == 270:
            self.dir = (-self.dir[1], self.dir[0])

    def do_waypoint_turn(self, deg: int):
        if deg % 360 == 90:
            self.waypoint = (self.waypoint[1], -self.waypoint[0])
        elif deg % 360 == 180:
            self.waypoint = (-self.waypoint[0], -self.waypoint[1])
        elif deg % 360 == 270:
            self.waypoint = (-self.waypoint[1], self.waypoint[0])


def get_test_input() -> str:
    return textwrap.dedent("""\
    F10
    N3
    F7
    R90
    F11""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines():
        data.append(Instruction(line))
    return data


def part_1(data):
    ship = Ship()
    for instr in data:
        ship.follow_1(instr)
    print('Part 1:', abs(ship.loc[0]) + abs(ship.loc[1]))


def part_2(data):
    ship = Ship()
    for instr in data:
        ship.follow_2(instr)
    print('Part 2:', abs(ship.loc[0]) + abs(ship.loc[1]))


def main():
    data = read_input(day_number=12, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
