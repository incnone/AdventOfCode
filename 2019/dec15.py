from intcode import IntcodeProgram
from enum import Enum
from typing import List


def add_pair(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


class DroidStatusCode(Enum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2

    def __str__(self):
        if self == DroidStatusCode.WALL:
            return '#'
        elif self == DroidStatusCode.MOVED:
            return ' '
        elif self == DroidStatusCode.OXYGEN:
            return 'O'


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def to_pair(self):
        if self == Direction.NORTH:
            return 0, -1
        elif self == Direction.SOUTH:
            return 0, 1
        elif self == Direction.WEST:
            return -1, 0
        elif self == Direction.EAST:
            return 1, 0

    def opposite(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.WEST:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.WEST


class RepairDroidAI(object):
    def __init__(self):
        self.explored = {(0, 0): DroidStatusCode.MOVED}
        self.loc = (0, 0)
        self.return_route = []     # type: List[Direction]
        self.desired_move_dir = None
        self.total_steps = 0

    @staticmethod
    def debug(s):
        debug = False
        if debug:
            print(s)

    def done_with_route(self):
        with open('input/dec15_out.txt', 'w') as file:
            file.write(self.get_map())
        self.fill_with_oxygen()
        exit(0)

    def fill_with_oxygen(self):
        # Dumb super-inefficient algorithm
        step = 0
        while any([x == DroidStatusCode.MOVED for x in self.explored.values()]):
            step += 1
            to_fill = set()
            for loc, tiletype in self.explored.items():
                if tiletype == DroidStatusCode.MOVED:
                    for direction in Direction:
                        adj_tile = add_pair(loc, direction.to_pair())
                        if adj_tile in self.explored and self.explored[adj_tile] == DroidStatusCode.OXYGEN:
                            to_fill.add(loc)

            for loc in to_fill:
                self.explored[loc] = DroidStatusCode.OXYGEN

        print('Full of oxygen at minute {}'.format(step))

    def move(self):
        if not self.return_route or self.desired_move_dir != self.return_route[-1]:
            self.return_route.append(self.desired_move_dir.opposite())
            self.total_steps += 1
        elif self.return_route:
            self.return_route.pop(-1)
            self.total_steps -= 1

        self.loc = add_pair(self.loc, self.desired_move_dir.to_pair())
        self.debug('{}, {}'.format(self.loc, self.return_route))

    def get_input(self):
        for direction in Direction:
            look_ahead = add_pair(self.loc, direction.to_pair())
            if look_ahead not in self.explored.keys():
                self.desired_move_dir = direction
                self.debug('INPUT: {}'.format(direction))
                return direction.value

        # If here, we don't have anywhere immediate to try to go, so back up.
        if self.return_route:
            backup_dir = self.return_route[-1]
            self.desired_move_dir = backup_dir
            self.debug('INPUT: (back up) {}'.format(backup_dir))
            return backup_dir.value

        # But if we can't back up, then we've fully explored everything
        else:
            self.done_with_route()

    def read_output(self, output):
        status = DroidStatusCode(output)
        self.debug('OUTPUT: {} {}'.format(status, add_pair(self.loc, self.desired_move_dir.to_pair())))
        self.explored[add_pair(self.loc, self.desired_move_dir.to_pair())] = status
        if status == DroidStatusCode.WALL:
            self.desired_move_dir = None
        elif status == DroidStatusCode.MOVED:
            self.move()
        elif status == DroidStatusCode.OXYGEN:
            self.move()
            print('Oxygen at step {}'.format(self.total_steps))     # This assumes maze is a tree

    def get_map(self):
        min_x = min([x[0] for x in self.explored.keys()])
        max_x = max([x[0] for x in self.explored.keys()])
        min_y = min([x[1] for x in self.explored.keys()])
        max_y = max([x[1] for x in self.explored.keys()])

        the_map = ''
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                if (x, y) == (0, 0):
                    the_map += 'S'
                elif (x, y) in self.explored.keys():
                    the_map += str(self.explored[(x, y)])
                else:
                    the_map += '?'
            the_map += '\n'
        return the_map


if __name__ == "__main__":
    with open('input/dec15.txt') as file:
        for line in file:
            program_code = line

    program = IntcodeProgram(program_code)
    droid_ai = RepairDroidAI()
    program.inputter = droid_ai
    program.outputter = droid_ai
    program.execute()
