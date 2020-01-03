from getinput import get_input
import itertools
import textwrap
from grid import Loc2, Direction
from typing import Dict, Optional
from collections import defaultdict


class ElfRoom(object):
    indicies = {
        Direction.NORTH: 0,
        Direction.WEST: 1,
        Direction.EAST: 2,
        Direction.SOUTH: 3
    }

    def __init__(self):
        self.dirs = [None, None, None, None]

    def __setitem__(self, key: Direction, value: Optional[bool]):
        self.dirs[ElfRoom.indicies[key]] = value

    def __getitem__(self, d: Direction):
        return self.dirs[ElfRoom.indicies[d]]

    def fill_with_doors(self):
        for idx in range(len(self.dirs)):
            if self.dirs[idx] is None:
                self.dirs[idx] = False


class ElfComplex(object):
    def __init__(self):
        self.rooms = defaultdict(lambda: ElfRoom())    # type: Dict[Loc2, ElfRoom]

    def __str__(self):
        xmin, xmax, ymin, ymax = self.bounds
        t = '#'
        for x in range(xmin, xmax+1):
            north = self.rooms[Loc2(x, ymin)][Direction.NORTH]
            if north is None: t += '?#'
            elif north is False: t += '##'
            elif north is True: t += '-#'
        t += '\n'

        for y in range(ymin, ymax+1):
            west = self.rooms[Loc2(xmin, y)][Direction.WEST]
            if west is None: line1 = '?'
            elif west is False: line1 = '#'
            else: line1 = '|'
            line2 = '#'
            for x in range(xmin, xmax+1):
                line1 += 'X' if Loc2(x, y) == Loc2(0, 0) else '.'
                south = self.rooms[Loc2(x, y)][Direction.SOUTH]
                east = self.rooms[Loc2(x, y)][Direction.EAST]

                if south is True: line2 += '-#'
                elif south is False: line2 += '##'
                elif south is None: line2 += '?#'

                if east is True: line1 += '|'
                elif east is False: line1 += '#'
                elif east is None: line1 += '?'

            line1 += '\n'
            line2 += '\n'
            t += line1 + line2
        return t

    @property
    def bounds(self):
        xmin = ymin = None
        xmax = ymax = None
        for loc in self.rooms.keys():
            xmin = min(loc.x, xmin) if xmin is not None else loc.x
            xmax = max(loc.x, xmax) if xmax is not None else loc.x
            ymin = min(loc.y, ymin) if ymin is not None else loc.y
            ymax = max(loc.y, ymax) if ymax is not None else loc.y
        return xmin, xmax, ymin, ymax

    @staticmethod
    def _ltr_to_dir(s: str):
        conv = {
            'N': Direction.NORTH,
            'W': Direction.WEST,
            'E': Direction.EAST,
            'S': Direction.SOUTH
        }
        return conv[s]

    @staticmethod
    def _get_path_split(s: str):
        """
        Break paren-paths into parts
        :param s: The string to be broken. Should have the form (a_1|a_2|...|a_n)b for strings a_i, b (where each
        of the a_i's is parenthesis-neutral).
        :return: [a_1, a_2, ..., a_n], index(b)
        """
        # Break paren-paths into parts
        assert s[0] == '('

        paths = []
        current_path = ''
        paren_depth = 0
        idx = 1
        for c in s[1:]:
            # note: idx points to the character AFTER c during this loop
            idx += 1
            if (c == '|' or c == ')') and paren_depth == 0:
                paths.append(current_path)
                current_path = ''
                if c == ')':
                    break
                continue

            if c == '(':
                paren_depth += 1
            elif c == ')':
                paren_depth -= 1
            current_path += c
            if paren_depth < 0:
                break
        return paths, idx

    def _explore_path_hlpr(self, s: str, start_loc: Loc2, cache, global_idx):
        current_loc = start_loc
        for idx, c in enumerate(s):
            if c == '^' or c == '$':
                pass
            elif c == '(':
                paths, end_idx = self._get_path_split(s[idx:])
                for path in paths:
                    self._explore_path_hlpr(path + s[idx+end_idx:], current_loc, cache, global_idx+idx)
                return
            else:
                d = self._ltr_to_dir(c)
                self.rooms[current_loc][d] = True
                current_loc = current_loc + d
                self.rooms[current_loc][d.opposite] = True

    def explore_path(self, s: str):
        return self._explore_path_hlpr(s, Loc2(0, 0), dict(), 0)

    def fill_with_doors(self):
        for v in self.rooms.values():
            v.fill_with_doors()

    def furthest_room_dist(self):
        explored = {Loc2(0, 0)}
        to_explore = [(Loc2(0, 0), 0)]
        max_dist = 0
        while to_explore:
            loc, dist = to_explore.pop()
            max_dist = max(max_dist, dist)
            room = self.rooms[loc]
            for d in Direction:
                if room[d]:
                    next_loc = loc + d
                    if next_loc not in explored:
                        to_explore.append((next_loc, dist+1))
                        explored.add(next_loc)
        return max_dist


def parse_input(s: str):
    return s


def part_1(input_str: str):
    input_str = test_input(2)
    complex = ElfComplex()
    complex.explore_path(input_str)
    complex.fill_with_doors()
    print(complex)
    return complex.furthest_room_dist()


def part_2(input_str: str):
    return


def test_input(test_num):
    if test_num == 1:
        return textwrap.dedent("""\
        ^ENWWW(NEEE|SSE(EE|N))$""")
    elif test_num == 2:
        return textwrap.dedent("""\
        ^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$""")
    elif test_num == 3:
        return textwrap.dedent("""\
        ^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$""")
    elif test_num == 4:
        return textwrap.dedent("""\
        ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$""")


def main():
    input_str = get_input(20)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
