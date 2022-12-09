import textwrap
import math
import itertools
from typing import List, Tuple, Iterable, Set
from enum import Enum


class Rotation(Enum):
    NONE = 0
    LEFT = 1
    HALF = 2
    RIGHT = 3

    def rotate(self, rot):
        return Rotation((self.value + rot.value) % 4)

    def comm(self):
        return Rotation((-self.value) % 4)


class Tile(object):
    @staticmethod
    def _upper_edge_s(data: List[List[bool]], rotation: Rotation, flip: bool) -> Iterable[bool]:
        if rotation == Rotation.NONE:
            return data[0] if not flip else reversed(data[0])
        elif rotation == Rotation.LEFT:
            return [row[-1] for row in data] if not flip else reversed([row[-1] for row in data])
        elif rotation == Rotation.HALF:
            return reversed(data[-1]) if not flip else data[-1]
        elif rotation == Rotation.RIGHT:
            return reversed([row[0] for row in data]) if not flip else [row[0] for row in data]

    @staticmethod
    def _ch(b: bool) -> str:
        return '#' if b else '.'

    def __init__(self, tile_id: int, data: List[List[bool]]):
        self.id = tile_id
        self.data = data
        self.rotation = Rotation.NONE
        self.flip = False   # Flip over y-axis after rotation
        self.w = len(data)

    def __str__(self):
        return self._str_hlpr(range(self.w))

    def __repr__(self):
        return f'<T{self.id}{self.rotation.name[0]}{"F" if self.flip else ""}>'

    def _str_hlpr(self, ran) -> str:
        if self.rotation == Rotation.NONE:
            if not self.flip:
                return '\n'.join(''.join(self._ch(self.data[j][i]) for i in ran) for j in ran)
            else:
                return '\n'.join(''.join(self._ch(self.data[j][-i-1]) for i in ran) for j in ran)
        elif self.rotation == Rotation.LEFT:
            if not self.flip:
                return '\n'.join(''.join(self._ch(self.data[i][-j-1]) for i in ran) for j in ran)
            else:
                return '\n'.join(''.join(self._ch(self.data[-i-1][-j-1]) for i in ran) for j in ran)
        elif self.rotation == Rotation.HALF:
            if not self.flip:
                return '\n'.join(''.join(self._ch(self.data[-j-1][-i-1]) for i in ran) for j in ran)
            else:
                return '\n'.join(''.join(self._ch(self.data[-j-1][i]) for i in ran) for j in ran)
        elif self.rotation == Rotation.RIGHT:
            if not self.flip:
                return '\n'.join(''.join(self._ch(self.data[-i-1][j]) for i in ran) for j in ran)
            else:
                return '\n'.join(''.join(self._ch(self.data[i][j]) for i in ran) for j in ran)

    def borderless_str(self) -> str:
        return self._str_hlpr(range(1, self.w - 1))

    def get_rotated(self, rot: Rotation, flip: bool):
        r = Tile(self.id, self.data)
        r.rotation = Rotation.rotate(self.rotation, rot if not self.flip else rot.comm())
        r.flip = self.flip ^ flip
        return r

    @property
    def top_edge(self) -> Iterable[bool]:
        return Tile._upper_edge_s(self.data, self.rotation, self.flip)

    @property
    def left_edge(self) -> Iterable[bool]:
        return Tile._upper_edge_s(
            self.data,
            self.rotation.rotate(Rotation.RIGHT if not self.flip else Rotation.LEFT),
            not self.flip
        )

    @property
    def bottom_edge(self) -> Iterable[bool]:
        return Tile._upper_edge_s(self.data, self.rotation.rotate(Rotation.HALF), not self.flip)

    @property
    def right_edge(self) -> Iterable[bool]:
        return Tile._upper_edge_s(
            self.data,
            self.rotation.rotate(Rotation.LEFT if not self.flip else Rotation.RIGHT),
            self.flip
        )

    def fits_right_of(self, other) -> bool:
        return list(self.left_edge) == list(other.right_edge)

    def fits_below(self, other) -> bool:
        return list(self.top_edge) == list(other.bottom_edge)


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for tile_str in s.split('\n\n'):
        lines = tile_str.splitlines()
        tile_id = int(lines[0].split()[1].rstrip(':'))
        tile_data = []
        for line in lines[1:]:
            tile_data.append([True if c == '#' else False for c in line.rstrip('\n')])
        data.append(Tile(tile_id, tile_data))
    return data


def valid_fills(partial_image: List[Tile], w: int, h: int, valid_tiles: List[Tile]) -> List[List[Tile]]:
    num_filled = len(partial_image)
    if num_filled == w*h:
        return [partial_image]

    valid_fills_list = []
    left_tile = partial_image[-1] if num_filled % w != 0 else None
    top_tile = partial_image[-w] if num_filled >= w else None
    for tile in valid_tiles:
        for rot in Rotation:
            for flip in [True, False]:
                rot_tile = tile.get_rotated(rot, flip)
                if (left_tile is None or rot_tile.fits_right_of(left_tile)) \
                        and (top_tile is None or rot_tile.fits_below(top_tile)):
                    valid_fills_list += \
                        valid_fills(partial_image + [rot_tile], w, h, [x for x in valid_tiles if x != tile])
    return valid_fills_list


def part_1(data):
    w = int(math.sqrt(len(data)))

    valid_fills_list = valid_fills([], w, w, data)
    assert len(valid_fills_list) == 8
    fill = valid_fills_list[0]
    print('Part 1:', fill[0].id*fill[w-1].id*fill[-w].id*fill[-1].id)


def cache_filename(test):
    return 'data/dec20_cache.txt' if not test else 'data/dec20_cache_test.txt'


def make_p2_cache(data, test):
    w = int(math.sqrt(len(data)))

    valid_fills_list = valid_fills([], w, w, data)
    assert len(valid_fills_list) == 8
    fill = valid_fills_list[0]

    lines_init = ('\n'.join(list(t.borderless_str() for t in fill))).splitlines(keepends=False)
    s = len(lines_init[0])
    filename = cache_filename(test)
    with open(filename, 'w') as file:
        for row in range(w*s):
            start_idx = (row // s) * w * s + row % s
            file.write(''.join(lines_init[c] for c in range(start_idx, start_idx + w * s, s)))
            file.write('\n')


def sea_monster_tiles(data: List[List[bool]], x: int, y: int, rot: Rotation, flip: bool) -> Set[Tuple[int, int]]:
    sea_monster_str = textwrap.dedent("""\
                      # 
    #    ##    ##    ###
     #  #  #  #  #  #   """)
    sea_monster = set()
    for jdx, line in enumerate(sea_monster_str.splitlines(keepends=False)):
        for idx, c in enumerate(line):
            if c == '#':
                if rot == Rotation.NONE:
                    sea_monster.add((idx, jdx) if not flip else (-idx, jdx))
                elif rot == Rotation.LEFT:
                    sea_monster.add((jdx, -idx) if not flip else (-jdx, -idx))
                if rot == Rotation.HALF:
                    sea_monster.add((-idx, -jdx) if not flip else (idx, -jdx))
                if rot == Rotation.RIGHT:
                    sea_monster.add((-jdx, idx) if not flip else (jdx, idx))

    all_tiles = set()
    temp_monster = set()
    found_all = True
    for offset in sea_monster:
        loc = (x + offset[0], y + offset[1])
        if 0 <= loc[1] < len(data) and 0 <= loc[0] < len(data[loc[1]]):
            found_all &= data[loc[1]][loc[0]]
        else:
            found_all = False
        temp_monster.add(loc)

    if found_all:
        all_tiles = all_tiles.union(temp_monster)

    return all_tiles


def part_2(test: bool):
    lines = []
    with open(cache_filename(test), 'r') as file:
        for line in file:
            lines.append(list(c == '#' for c in line))

    w = len(lines[0])
    h = len(lines)
    sm_tiles = set()
    for x, y, rot, flip in itertools.product(range(w), range(h), Rotation, [False, True]):
        sm_tiles = sm_tiles.union(sea_monster_tiles(lines, x, y, rot, flip))

    num_water = sum(sum(1 if c else 0 for c in line) for line in lines)
    print('Part 2:', num_water - len(sm_tiles))


def main():
    test = False
    data = read_input(day_number=20, test=test)
    # part_1(data)
    # make_p2_cache(data, test)
    part_2(test)


def get_test_input() -> str:
    return textwrap.dedent("""\
    Tile 2311:
    ..##.#..#.
    ##..#.....
    #...##..#.
    ####.#...#
    ##.##.###.
    ##...#.###
    .#.#.#..##
    ..#....#..
    ###...#.#.
    ..###..###

    Tile 1951:
    #.##...##.
    #.####...#
    .....#..##
    #...######
    .##.#....#
    .###.#####
    ###.##.##.
    .###....#.
    ..#.#..#.#
    #...##.#..

    Tile 1171:
    ####...##.
    #..##.#..#
    ##.#..#.#.
    .###.####.
    ..###.####
    .##....##.
    .#...####.
    #.##.####.
    ####..#...
    .....##...

    Tile 1427:
    ###.##.#..
    .#..#.##..
    .#.##.#..#
    #.#.#.##.#
    ....#...##
    ...##..##.
    ...#.#####
    .#.####.#.
    ..#..###.#
    ..##.#..#.

    Tile 1489:
    ##.#.#....
    ..##...#..
    .##..##...
    ..#...#...
    #####...#.
    #..#.#.#.#
    ...#.#.#..
    ##.#...##.
    ..##.##.##
    ###.##.#..

    Tile 2473:
    #....####.
    #..#.##...
    #.##..#...
    ######.#.#
    .#...#.#.#
    .#########
    .###.#..#.
    ########.#
    ##...##.#.
    ..###.#.#.

    Tile 2971:
    ..#.#....#
    #...###...
    #.#.###...
    ##.##..#..
    .#####..##
    .#..####.#
    #..#.#..#.
    ..####.###
    ..#.#.###.
    ...#.#.#.#

    Tile 2729:
    ...#.#.#.#
    ####.#....
    ..#.#.....
    ....#..#.#
    .##..##.#.
    .#.####...
    ####.#.#..
    ##.####...
    ##..#.##..
    #.##...##.

    Tile 3079:
    #.#.#####.
    .#..######
    ..#.......
    ######....
    ####.#..#.
    .#...#.##.
    #.#####.##
    ..#.###...
    ..#.......
    ..#.###...""")


if __name__ == "__main__":
    main()
