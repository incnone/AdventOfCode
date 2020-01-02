from getinput import get_input
import itertools
import textwrap
from grid import Loc2, Loc2Grid, Direction
import unittest


class Combatant(object):
    elf_index = 0
    goblin_index = 0

    @staticmethod
    def elf(loc, battle):
        Combatant.elf_index += 1
        return Combatant('Elf-{}'.format(Combatant.elf_index), 3, 200, loc, battle)

    @staticmethod
    def goblin(loc, battle):
        Combatant.elf_index += 1
        return Combatant('Gob-{}'.format(Combatant.goblin_index), 3, 200, loc, battle)

    def __init__(self, name, damage, hp, loc, battle):
        self.name = name
        self.damage = damage
        self.hp = hp
        self.loc = loc
        self.battle = battle

    def __str__(self):
        return '{}({})'.format(self.letter, self.hp)

    @property
    def sortkey(self):
        return self.loc.y, self.loc.x

    @property
    def letter(self):
        return self.name[0]

    def target_at(self, loc):
        target_letters = {'E': 'G', 'G': 'E'}
        target_ltr = target_letters[self.letter]
        for c in self.battle.combatants:
            if c.loc == loc and c.letter == target_ltr:
                return c
        return None

    def move(self):
        direction_order = [Direction.NORTH, Direction.WEST, Direction.EAST, Direction.SOUTH]

        # Look for the closest squares which are adjacent to enemies
        old_tiles = [self.loc]
        searched = {self.loc}
        paths = {self.loc: []}
        dist = 0
        desireable_squares = set()
        while old_tiles and not desireable_squares:
            dist += 1
            new_tiles = []
            for p, d in itertools.product(old_tiles, direction_order):
                new_loc = p + d
                if new_loc not in searched:
                    searched.add(new_loc)
                    if self.battle.passable(new_loc):
                        new_tiles.append(new_loc)
                        paths[new_loc] = paths[p] + [new_loc]
                if self.target_at(new_loc) is not None:
                    desireable_squares.add(p)
            old_tiles = new_tiles

        if not desireable_squares or self.loc in desireable_squares:
            return
        else:
            self.loc = min(
                [(v[0], k) for k, v in paths.items() if k in desireable_squares],
                key=lambda q: (q[1].y, q[1].x)
            )[0]

    def attack(self):
        # "Dead" units will show up here, so be careful (test for positive hp)
        if self.hp <= 0:
            return

        targets = []
        for p in [self.loc + d for d in Direction]:
            target = self.target_at(p)
            if target is not None and target.hp > 0:
                targets.append(target)

        if targets:
            target = min(targets, key=lambda c: (c.hp, c.loc.y, c.loc.x))
            target.hp -= self.damage
            # print('Unit at {} attacks unit at {}'.format(self.loc, target.loc))


class Battle(object):
    def __init__(self, s):
        self.ticks = 0
        self.arena = Loc2Grid(
            list(list(True if c == '#' else False for c in line) for line in s.splitlines(keepends=False))
        )
        self.combatants = []
        for y, line in enumerate(s.splitlines(keepends=False)):
            for x, c in enumerate(line):
                if c == 'E':
                    self.combatants.append(Combatant.elf(Loc2(x, y), self))
                elif c == 'G':
                    self.combatants.append(Combatant.goblin(Loc2(x, y), self))

    def _get_char(self, loc):
        for combatant in self.combatants:
            if combatant.loc == loc:
                return combatant.letter
        return '#' if self.arena.at(loc) else '.'

    def __str__(self):
        return '\n'.join(
            ''.join(self._get_char(Loc2(x, y)) for x in range(len(line))) for y, line in enumerate(self.arena.arr)
        )

    def passable(self, loc):
        return not self.arena.at(loc) and not any(c.loc == loc for c in self.combatants)

    def tick(self):
        self.combatants = sorted(self.combatants, key=lambda c: c.sortkey)
        for combatant in self.combatants:
            if not self.active:
                break
            combatant.move()
            combatant.attack()
        else:
            self.ticks += 1
        self.combatants[:] = [c for c in self.combatants if c.hp > 0]

    @property
    def active(self):
        return any(c.letter == 'E' and c.hp > 0 for c in self.combatants) \
               and any(c.letter == 'G' and c.hp > 0 for c in self.combatants)

    @property
    def outcome(self):
        return self.ticks*sum(c.hp for c in self.combatants)


def get_outcome(battle):
    while battle.active:
        battle.tick()
    return battle.outcome


def step_through(battle):
    while battle.active:
        print('----{}----'.format(battle.ticks))
        print(battle)
        print(' / '.join(str(c.hp) for c in battle.combatants))
        input()
        battle.tick()
    print('----{}----'.format(battle.ticks))
    print(battle)


def part_1(input_str: str):
    input_str = textwrap.dedent("""\
    #########
    #.......#
    #.......#
    #E..G...#
    #..GE...#
    #.#.#...#
    #.#.#####
    #.#...E.#
    #########""")

    step_through(Battle(input_str))
    return get_outcome(Battle(input_str))


def part_2(input_str: str):
    return


class TestBattle(unittest.TestCase):
    def test_1(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #EG...#
        #####.#
        #..E..#
        #.#####
        #...G.#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(1751, outcome)
        self.assertEqual(healths, [17])

    def test_2(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(27730, outcome)
        self.assertEqual(healths, [200, 131, 59, 200])

    def test_3(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #G..#E#
        #E#E.E#
        #G.##.#
        #...#E#
        #...E.#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(36334, outcome)
        self.assertEqual(healths, [200, 197, 185, 200, 200])

    def test_4(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #E..EG#
        #.#G.E#
        #E.##E#
        #G..#.#
        #..E#.#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(39514, outcome)
        self.assertEqual(healths, [164, 197, 200, 98, 200])

    def test_5(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #E.G#.#
        #.#G..#
        #G.#.G#
        #G..#.#
        #...E.#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(27755, outcome)
        self.assertEqual(healths, [200, 98, 200, 95, 200])

    def test_6(self):
        battle = Battle(textwrap.dedent("""\
        #######
        #.E...#
        #.#..G#
        #.###.#
        #E#G#G#
        #...#G#
        #######"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(28944, outcome)
        self.assertEqual(healths, [200, 98, 38, 200])

    def test_7(self):
        battle = Battle(textwrap.dedent("""\
        #########
        #G......#
        #.E.#...#
        #..##..G#
        #...##..#
        #...#...#
        #.G...G.#
        #.....G.#
        #########"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(18740, outcome)
        self.assertEqual(healths, [137, 200, 200, 200, 200])

    def test_8(self):
        battle = Battle(textwrap.dedent("""\
        #########
        #.......#
        #.......#
        #E..G...#
        #..GE...#
        #.#.#...#
        #.#.#####
        #.#...E.#
        #########"""))
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(18020, outcome)


def main():
    input_str = get_input(15)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    unittest.main()
    main()
