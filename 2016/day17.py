from getinput import get_input
from grid import Direction, Loc2
import hashlib
from priorityqueue import PriorityQueue


def dir_char(direction: Direction):
    thedict = {
        Direction.NORTH: 'U',
        Direction.SOUTH: 'D',
        Direction.WEST: 'L',
        Direction.EAST: 'R',
    }
    return thedict[direction]


def get_hash(salt, path):
    hash_str = salt + ''.join(dir_char(d) for d in path)
    return hashlib.md5(hash_str.encode('utf-8')).hexdigest()


def open_door_char(c):
    return 'b' <= c <= 'f'


class Path(object):
    def __init__(self, path):
        self.path = path
        self.loc = Loc2(0, 0)
        for d in self.path:
            self.loc = self.loc + d

    @property
    def is_exit(self):
        return self.loc == Loc2(3, 3)


def get_open_doors(salt, path):
    the_hash = get_hash(salt, path.path)
    open_doors = set()
    if open_door_char(the_hash[0]) and path.loc.y > 0:
        open_doors.add(Direction.NORTH)
    if open_door_char(the_hash[1]) and path.loc.y < 3:
        open_doors.add(Direction.SOUTH)
    if open_door_char(the_hash[2]) and path.loc.x > 0:
        open_doors.add(Direction.WEST)
    if open_door_char(the_hash[3]) and path.loc.x < 3:
        open_doors.add(Direction.EAST)
    return open_doors


def find_shortest_route(salt):
    pq = PriorityQueue()
    pq.add_task(Path([]), priority=0)
    while pq:
        dist, path = pq.pop_task_with_priority()
        if path.is_exit:
            return dist, path
        dirs = get_open_doors(salt, path)
        for d in dirs:
            new_path = Path(path.path + [d])
            pq.add_task_if_better(new_path, priority=dist+1)


def find_longest_route(salt):
    pq = PriorityQueue()
    pq.add_task(Path([]), priority=0)
    dists_to_exit = []
    last_dist = None
    while pq:
        dist, path = pq.pop_task_with_priority()
        if dist != last_dist:
            print(dist)
            last_dist = dist
        if path.is_exit:
            dists_to_exit.append(dist)
            continue
        dirs = get_open_doors(salt, path)
        for d in dirs:
            new_path = Path(path.path + [d])
            pq.add_task_if_better(new_path, priority=dist+1)
    return max(dists_to_exit)


def part_1(big_str):
    dist, path = find_shortest_route(big_str)
    return ''.join(dir_char(c) for c in path.path)


def part_2(big_str):
    return find_longest_route(big_str)


if __name__ == "__main__":
    the_big_str = get_input(17)

    # print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
