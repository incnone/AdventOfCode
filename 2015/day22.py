from getinput import get_input
from wizard import *
import heapq
import itertools
import copy


def get_min_mana(hard_mode):
    attempts = [Fight(hard_mode)]
    while attempts[0].enemy_hp > 0:
        fight = heapq.heappop(attempts)
        for next_spell in PlayerAction:
            new_fight = copy.copy(fight)    # type: Fight
            try:
                new_fight.do_turn(next_spell)
                heapq.heappush(attempts, new_fight)
            except BadAction:
                continue
    return attempts[0].spent_mana


def part_1():
    return get_min_mana(hard_mode=False)


def part_2():
    return get_min_mana(hard_mode=True)


if __name__ == "__main__":
    print('Part 1:', part_1())
    print('Part 2:', part_2())
