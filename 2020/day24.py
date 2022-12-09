import textwrap


class HexTileGrid(object):
    """
    Hex coordinate convention: (1,0) = East, (0, 1) = Northeast
    """
    adjacency_offsets = [(-1, 1), (0, 1), (-1, 0), (1, 0), (0, -1), (1, -1)]

    @staticmethod
    def parse_dir_str(s: str):
        dirs = []
        c = iter(s)
        while True:
            try:
                val = next(c)
                if val == 'n':
                    nextval = next(c)
                    if nextval == 'e':
                        dirs.append((0, 1))
                    elif nextval == 'w':
                        dirs.append((-1, 1))
                    else:
                        raise RuntimeError(f'Bad dir string: {s}')
                elif val == 's':
                    nextval = next(c)
                    if nextval == 'e':
                        dirs.append((1, -1))
                    elif nextval == 'w':
                        dirs.append((0, -1))
                    else:
                        raise RuntimeError(f'Bad dir string: {s}')
                elif val == 'w':
                    dirs.append((-1, 0))
                elif val == 'e':
                    dirs.append((1, 0))
                else:
                    raise RuntimeError(f'Bad dir string: {s}')
            except StopIteration:
                break
        return dirs

    def __init__(self, s: str):
        self.flipped_tiles = set()
        for line in s.splitlines(keepends=False):
            dirs = HexTileGrid.parse_dir_str(line)
            loc = (0, 0)
            for d in dirs:
                loc = (loc[0] + d[0], loc[1] + d[1])
            if loc in self.flipped_tiles:
                self.flipped_tiles.remove(loc)
            else:
                self.flipped_tiles.add(loc)

    def __str__(self):
        return self.flipped_tiles

    @property
    def num_flipped(self):
        return len(self.flipped_tiles)

    def num_adjacent(self, loc):
        tot = 0
        for p in HexTileGrid.adjacency_offsets:
            if (loc[0] + p[0], loc[1] + p[1]) in self.flipped_tiles:
                tot += 1
        return tot

    def step(self):
        new_flipped = set()
        tiles_to_check = set()
        for tile in self.flipped_tiles:
            tiles_to_check.add(tile)
            for p in HexTileGrid.adjacency_offsets:
                tiles_to_check.add((tile[0] + p[0], tile[1] + p[1]))
        for tile in tiles_to_check:
            num_adj = self.num_adjacent(tile)
            if tile in self.flipped_tiles:
                if 1 <= num_adj <= 2:
                    new_flipped.add(tile)
            else:
                if num_adj == 2:
                    new_flipped.add(tile)
        self.flipped_tiles = new_flipped


def get_test_input() -> str:
    return textwrap.dedent("""\
    sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return s


def part_1(data):
    grid = HexTileGrid(data)
    print('Part 1: ', grid.num_flipped)


def part_2(data):
    grid = HexTileGrid(data)
    for _ in range(100):
        grid.step()
    print('Part 2: ', grid.num_flipped)


def main():
    data = read_input(day_number=24, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
