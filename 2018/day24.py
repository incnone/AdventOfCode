from getinput import get_input
import itertools
import textwrap
import re
from enum import Enum


class BattleSide(Enum):
    IMMUNE = 0
    INFECTION = 1


class Battle(object):
    idx = 0
    atk_type_str_to_int = dict()
    atk_type_int_to_str = dict()

    @staticmethod
    def get_attack_type(s):
        if s in Battle.atk_type_str_to_int:
            return Battle.atk_type_str_to_int[s]
        else:
            Battle.atk_type_str_to_int[s] = Battle.idx
            Battle.atk_type_int_to_str[Battle.idx] = s
            Battle.idx += 1
            return Battle.idx - 1

    @staticmethod
    def get_attack_str(x):
        if x is None:
            return 'none'
        return Battle.atk_type_int_to_str[x]

    def __init__(self, groups):
        self.groups = groups
        self.stall_counter = 0

    def get_target(self, g, targets):
        allowable_targets = [x for x in self.groups if x.side != g.side and x not in targets.values()]
        if not allowable_targets:
            return None
        else:
            return max(allowable_targets, key=lambda x: (g.get_damage_to(x), g.effective_power, g.initiative))

    def get_targets(self):
        targets = dict()
        self.groups = sorted(self.groups, key=lambda x: (x.effective_power, x.initiative), reverse=True)
        for g in self.groups:
            targets[g] = self.get_target(g, targets)
        return targets

    def immune_boost(self, boost):
        for g in self.groups:
            if g.side == BattleSide.IMMUNE:
                g.attack_dmg += boost

    def run(self):
        while any(g.side == BattleSide.IMMUNE for g in self.groups) \
                and any(g.side == BattleSide.INFECTION for g in self.groups):
            self.step()
            if self.stall_counter >= 10:
                return None
        if any(g.side == BattleSide.IMMUNE for g in self.groups):
            return BattleSide.IMMUNE
        else:
            return BattleSide.INFECTION

    def step(self):
        targets = self.get_targets()
        self.do_attacks(targets)

    def do_attacks(self, targets):
        any_damage = False
        attackers = sorted(targets.keys(), key=lambda x: x.initiative, reverse=True)
        for attacker in attackers:
            if attacker.num_units <= 0:
                continue
            target = targets[attacker]
            if target is None:
                continue
            damage = attacker.get_damage_to(target)
            num_dead = damage // target.hp
            if num_dead > 0:
                any_damage = True
            target.num_units -= num_dead
        self.groups = [g for g in self.groups if g.num_units > 0]
        if not any_damage:
            self.stall_counter += 1
        else:
            self.stall_counter = 0


class Group(object):
    def __init__(self, num_units, hp, immunities, weaknesses, atk_dmg, atk_type, initiative, side):
        self.num_units = int(num_units)
        self.hp = int(hp)
        self.immunities = list(Battle.get_attack_type(s) for s in immunities)
        self.weaknesses = list(Battle.get_attack_type(s) for s in weaknesses)
        self.attack_dmg = int(atk_dmg)
        self.attack_type = Battle.get_attack_type(atk_type)
        self.initiative = int(initiative)
        self.side = side

    def __str__(self):
        return '{side} {n} units (HP: {hp}, atk: {atk} ({atk_type}), init: {init}, immune: {imm}, weak: {wk})'.format(
            side='Immune' if self.side == BattleSide.IMMUNE else 'Infection',
            n=self.num_units,
            hp=self.hp,
            atk=self.attack_dmg,
            atk_type=Battle.get_attack_str(self.attack_type),
            init=self.initiative,
            imm=list(Battle.get_attack_str(x) for x in self.immunities),
            wk=list(Battle.get_attack_str(x) for x in self.weaknesses)
        )

    def __repr__(self):
        return str(self)

    @property
    def effective_power(self):
        return self.num_units*self.attack_dmg

    def get_damage_to(self, other):
        if self.side == other.side:
            return 0
        factor = 1
        if self.attack_type in other.immunities:
            factor = 0
        if self.attack_type in other.weaknesses:
            factor = 2
        return self.effective_power*factor


def parse_input(s: str):
    immune_system = True
    groups = []
    for line in s.splitlines(keepends=False):
        if not line:
            continue
        if line.startswith('Infection'):
            immune_system = False
            continue
        if line.startswith('Immune'):
            continue
        units, hp = re.findall(r'(\d*) units each with (\d*) hit points', line)[0]
        immunities_re = re.findall(r'immune to ([^;\)]*)', line)
        weaknesses_re = re.findall(r'weak to ([^;\)]*)', line)
        immunities = []
        weaknesses = []
        if immunities_re:
            immunities = [x.strip() for x in immunities_re[0].split(',')]
        if weaknesses_re:
            weaknesses = [x.strip() for x in weaknesses_re[0].split(',')]
        atk_dmg, atk_type, init = re.findall(r'(\d*) (\w*) damage at initiative (\d*)', line)[0]
        side = BattleSide.IMMUNE if immune_system else BattleSide.INFECTION
        group = Group(num_units=units, hp=hp, immunities=immunities, weaknesses=weaknesses, atk_dmg=atk_dmg,
                      atk_type=atk_type, initiative=init, side=side)
        groups.append(group)
    return Battle(groups=groups)


def part_1(input_str: str):
    # input_str = test_input()
    battle = parse_input(input_str)
    battle.run()
    return sum(g.num_units for g in battle.groups)


def get_winner(input_str, boost: int):
    battle = parse_input(input_str)
    battle.immune_boost(boost)
    return battle.run()


def part_2(input_str: str):
    # input_str = test_input()

    for boost in range(40850, 47000):
        if boost % 10 == 0:
            print(boost)
        battle = parse_input(input_str)
        battle.immune_boost(boost)
        winner = battle.run()
        if winner == BattleSide.IMMUNE:
            print(boost)
            return sum(g.num_units for g in battle.groups)

    # min_boost = 0
    # max_boost = 100000
    # assert get_winner(input_str, min_boost) != BattleSide.IMMUNE
    # assert get_winner(input_str, max_boost) == BattleSide.IMMUNE
    #
    # while max_boost - min_boost > 1:
    #     half_boost = (max_boost + min_boost) // 2
    #     winner = get_winner(input_str, half_boost)
    #     if winner == BattleSide.IMMUNE:
    #         max_boost = half_boost
    #     else:
    #         min_boost = half_boost
    #
    # battle = parse_input(input_str)
    # battle.immune_boost(max_boost)
    # battle.run()
    # return sum(g.num_units for g in battle.groups)


def test_input():
    return textwrap.dedent("""\
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3
    
    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""")


def main():
    input_str = get_input(24)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
