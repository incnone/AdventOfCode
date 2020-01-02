from getinput import get_input
import itertools
import textwrap
from grid import Loc2, Loc2Grid, Direction
import unittest
from copy import copy


class Combatant(object):
    elf_index = 0
    goblin_index = 0

    @staticmethod
    def elf(loc, battle, damage=3, hp=200):
        Combatant.elf_index += 1
        return Combatant('Elf-{}'.format(Combatant.elf_index), damage, hp, loc, battle)

    @staticmethod
    def goblin(loc, battle, damage=3, hp=200):
        Combatant.elf_index += 1
        return Combatant('Gob-{}'.format(Combatant.goblin_index), damage, hp, loc, battle)

    def __init__(self, name, damage, hp, loc, battle):
        self.name = name
        self.damage = damage
        self.hp = hp
        self.loc = loc
        self.battle = battle

    def __str__(self):
        return '{}({})'.format(self.letter, self.hp)

    def __copy__(self):
        raise NotImplementedError()

    def get_copy(self, battle):
        return Combatant(self.name, self.damage, self.hp, self.loc, battle)

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
            if c.loc == loc and c.letter == target_ltr and c.alive:
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

    @property
    def alive(self):
        return self.hp > 0


class Battle(object):
    def __init__(self, s, elf_damage=3):
        # Might be more efficient to keep a map of locations to combatants (to more easily answer the
        # common question "What's on this tile?")
        self.ticks = 0
        self.arena = Loc2Grid(
            list(list(True if c == '#' else False for c in line) for line in s.splitlines(keepends=False))
        )
        self.combatants = []
        for y, line in enumerate(s.splitlines(keepends=False)):
            for x, c in enumerate(line):
                if c == 'E':
                    self.combatants.append(Combatant.elf(Loc2(x, y), self, damage=elf_damage))
                elif c == 'G':
                    self.combatants.append(Combatant.goblin(Loc2(x, y), self))

    def __copy__(self):
        raise NotImplementedError()
        # battle = Battle('')
        # battle.arena = self.arena
        # battle.ticks = self.ticks
        # for c in self.combatants:
        #     battle.combatants.append(c.get_copy(battle))
        # return battle

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
        return not self.arena.at(loc) and not any((c.loc == loc and c.alive) for c in self.combatants)

    def tick(self):
        self.combatants = sorted(self.combatants, key=lambda c: c.sortkey)
        for combatant in self.combatants:
            if not self.active:
                break
            combatant.move()
            combatant.attack()
        else:
            self.ticks += 1
        self.combatants[:] = [c for c in self.combatants if c.alive]

    @property
    def active(self):
        return any(c.letter == 'E' and c.alive for c in self.combatants) \
               and any(c.letter == 'G' and c.alive for c in self.combatants)

    @property
    def outcome(self):
        return self.ticks*sum(c.hp for c in self.combatants)

    @property
    def winner(self):
        elves = any(c.letter == 'E' and c.alive for c in self.combatants)
        gobs = any(c.letter == 'G' and c.alive for c in self.combatants)
        if elves and not gobs:
            return 'E'
        elif gobs and not elves:
            return 'G'
        else:
            return None


def get_outcome(battle):
    while battle.active:
        battle.tick()
    return battle.outcome


def get_narrowest_elf_win_outcome(battle_str):
    elf_damage = 2
    while True:
        elf_damage += 1
        battle = Battle(battle_str, elf_damage=elf_damage)
        num_elves = sum(1 for c in battle.combatants if c.letter == 'E')
        outcome = get_outcome(battle)
        if num_elves == sum(1 for c in battle.combatants if c.letter == 'E'):
            break

    return outcome


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
    return get_outcome(Battle(input_str))


def part_2(input_str: str):
    return get_narrowest_elf_win_outcome(input_str)


class TestBattle(unittest.TestCase):
    def test_1(self):
        battle_str = textwrap.dedent("""\
        #######
        #EG...#
        #####.#
        #..E..#
        #.#####
        #...G.#
        #######""")
        battle_1 = Battle(battle_str)
        outcome = get_outcome(battle_1)
        self.assertEqual(1751, outcome)

    def test_2(self):
        battle_str = textwrap.dedent("""\
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        self.assertEqual(27730, outcome)
        self.assertEqual(4988, get_narrowest_elf_win_outcome(battle_str))

    def test_3(self):
        battle_str = textwrap.dedent("""\
        #######
        #G..#E#
        #E#E.E#
        #G.##.#
        #...#E#
        #...E.#
        #######""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(36334, outcome)
        self.assertEqual(healths, [200, 197, 185, 200, 200])

    def test_4(self):
        battle_str = textwrap.dedent("""\
        #######
        #E..EG#
        #.#G.E#
        #E.##E#
        #G..#.#
        #..E#.#
        #######""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(39514, outcome)
        self.assertEqual(healths, [164, 197, 200, 98, 200])
        self.assertEqual(31284, get_narrowest_elf_win_outcome(battle_str))

    def test_5(self):
        battle_str = textwrap.dedent("""\
        #######
        #E.G#.#
        #.#G..#
        #G.#.G#
        #G..#.#
        #...E.#
        #######""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(27755, outcome)
        self.assertEqual(healths, [200, 98, 200, 95, 200])
        self.assertEqual(3478, get_narrowest_elf_win_outcome(battle_str))

    def test_6(self):
        battle_str = textwrap.dedent("""\
        #######
        #.E...#
        #.#..G#
        #.###.#
        #E#G#G#
        #...#G#
        #######""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(28944, outcome)
        self.assertEqual(healths, [200, 98, 38, 200])
        self.assertEqual(6474, get_narrowest_elf_win_outcome(battle_str))

    def test_7(self):
        battle_str = textwrap.dedent("""\
        #########
        #G......#
        #.E.#...#
        #..##..G#
        #...##..#
        #...#...#
        #.G...G.#
        #.....G.#
        #########""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        healths = [c.hp for c in battle.combatants]
        self.assertEqual(18740, outcome)
        self.assertEqual(healths, [137, 200, 200, 200, 200])
        self.assertEqual(1140, get_narrowest_elf_win_outcome(battle_str))

    def test_8(self):
        battle_str = textwrap.dedent("""\
        #########
        #.......#
        #.......#
        #E..G...#
        #..GE...#
        #.#.#...#
        #.#.#####
        #.#...E.#
        #########""")
        battle = Battle(battle_str)
        outcome = get_outcome(battle)
        self.assertEqual(18020, outcome)


def main():
    input_str = get_input(15)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    # unittest.main()
    main()
