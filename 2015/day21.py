from getinput import get_input
from enum import Enum
import itertools


class BossStats(object):
    def __init__(self):
        self.hp = None
        self.damage = None
        self.armor = None


class ItemType(Enum):
    WEAPON = 0
    ARMOR = 1
    RING = 2


class Item(object):
    def __init__(self, name, cost, damage, armor, t):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor
        self.item_type = t

    def __str__(self):
        return '${}: [{}]{} -- {}/{}'.format(self.cost, self.item_type.name, self.name, self.damage, self.armor)


class Build(object):
    def __init__(self, items):
        self.cost = 0
        self.damage = 0
        self.armor = 0
        for i in items:
            self.cost += i.cost
            self.damage += i.damage
            self.armor += i.armor

    def __str__(self):
        return '${}: -- {}/{}'.format(self.cost, self.damage, self.armor)


def player_wins(build: Build, boss: BossStats):
    boss_hp = boss.hp
    player_hp = 100

    while True:
        boss_hp -= max(1, build.damage - boss.armor)
        if boss_hp <= 0:
            return True
        player_hp -= max(1, boss.damage - build.armor)
        if player_hp <= 0:
            return False


def parse_input(s):
    boss = BossStats()
    items = []
    item_type = None
    for line in s.splitlines(keepends=False):
        words = line.split()
        if not words:
            continue

        if words[0] == 'Weapons:':
            item_type = ItemType.WEAPON
        elif words[0] == 'Armor:' and len(words) == 4:
            item_type = ItemType.ARMOR
        elif words[0] == 'Rings:':
            item_type = ItemType.RING

        # Boss/item info
        else:
            # Boss stuff
            if item_type is None:
                if words[0].startswith('Hit'):
                    boss.hp = int(words[-1])
                elif words[0].startswith('Dam'):
                    boss.damage = int(words[-1])
                elif words[0].startswith('Arm'):
                    boss.armor = int(words[-1])

            # Items
            else:
                items.append(Item(
                    name=' '.join(words[0:-3]),
                    cost=int(words[-3]),
                    damage=int(words[-2]),
                    armor=int(words[-1]),
                    t=item_type,
                ))

    return boss, items


def part_1(boss_stats, items):
    weapons = list(i for i in items if i.item_type == ItemType.WEAPON)
    armors = list(i for i in items if i.item_type == ItemType.ARMOR)
    rings = list(i for i in items if i.item_type == ItemType.RING)

    no_armor = Item(name='Empty', cost=0, damage=0, armor=0, t=ItemType.ARMOR)
    no_ring = Item(name='Empty', cost=0, damage=0, armor=0, t=ItemType.RING)
    armors.append(no_armor)
    rings.append(no_ring)

    min_cost = 9999999999
    for weapon, armor, ring_1, ring_2 in itertools.product(weapons, armors, rings, rings):
        if ring_1 == ring_2 and ring_1 != no_ring:
            continue
        build = Build([weapon, armor, ring_1, ring_2])
        if player_wins(build, boss_stats):
            min_cost = min(min_cost, build.cost)
    return min_cost


def part_2(boss_stats, items):
    weapons = list(i for i in items if i.item_type == ItemType.WEAPON)
    armors = list(i for i in items if i.item_type == ItemType.ARMOR)
    rings = list(i for i in items if i.item_type == ItemType.RING)

    no_armor = Item(name='Empty', cost=0, damage=0, armor=0, t=ItemType.ARMOR)
    no_ring = Item(name='Empty', cost=0, damage=0, armor=0, t=ItemType.RING)
    armors.append(no_armor)
    rings.append(no_ring)

    max_cost = 0
    for weapon, armor, ring_1, ring_2 in itertools.product(weapons, armors, rings, rings):
        if ring_1 == ring_2 and ring_1 != no_ring:
            continue
        build = Build([weapon, armor, ring_1, ring_2])
        if not player_wins(build, boss_stats):
            max_cost = max(max_cost, build.cost)
    return max_cost


if __name__ == "__main__":
    the_boss_stats, the_items = parse_input(get_input(21))

    print('Part 1:', part_1(the_boss_stats, the_items))
    print('Part 2:', part_2(the_boss_stats, the_items))
