from enum import Enum


class BadAction(RuntimeError):
    def __init__(self, *args):
        RuntimeError.__init__(self, *args)


class PlayerAction(Enum):
    MAGIC_MISSILE = 0
    DRAIN = 1
    SHIELD = 2
    POISON = 3
    RECHARGE = 4


class Fight(object):
    def __init__(self, hard_mode):
        # Player data
        self.player_hp = 50 if not hard_mode else 49
        self.player_mana = 500
        self.spent_mana = 0

        # Enemy
        self.enemy_hp = 51
        self.enemy_damage = 9

        # Effects
        self.poison = 0
        self.shield = 0
        self.recharge = 0

        # Hard mode
        self.hard_mode = hard_mode

        # Fight logging
        self._log = []

    def __lt__(self, other):
        return self.spent_mana < other.spent_mana

    def cast_spell(self, action):
        if action == PlayerAction.MAGIC_MISSILE:
            mana_cost = 53
            if self.player_mana < mana_cost:
                raise BadAction('Not enough mana for Magic Missile.')
            self.enemy_hp -= 4
            self.player_mana -= mana_cost
            self.spent_mana += mana_cost
        elif action == PlayerAction.DRAIN:
            mana_cost = 73
            if self.player_mana < mana_cost:
                raise BadAction('Not enough mana for Drain.')
            self.enemy_hp -= 2
            self.player_hp += 2
            self.player_mana -= mana_cost
            self.spent_mana += mana_cost
        elif action == PlayerAction.SHIELD:
            mana_cost = 113
            if self.shield > 0:
                raise BadAction('Shield already in effect.')
            if self.player_mana < mana_cost:
                raise BadAction('Not enough mana for Shield.')
            self.shield = 6
            self.player_mana -= mana_cost
            self.spent_mana += mana_cost
        elif action == PlayerAction.POISON:
            mana_cost = 173
            if self.poison > 0:
                raise BadAction('Poison already in effect.')
            if self.player_mana < mana_cost:
                raise BadAction('Not enough mana for Poison.')
            self.poison = 6
            self.player_mana -= mana_cost
            self.spent_mana += mana_cost
        elif action == PlayerAction.RECHARGE:
            mana_cost = 229
            if self.recharge > 0:
                raise BadAction('Recharge already in effect.')
            if self.player_mana < mana_cost:
                raise BadAction('Not enough mana for Recharge.')
            self.recharge = 5
            self.player_mana -= mana_cost
            self.spent_mana += mana_cost

    def manage_effects(self):
        if self.poison > 0:
            self.poison -= 1
            self.enemy_hp -= 3
            self.log('Poison deals {} damage; its timer is now {}.'.format(3, self.poison))
        if self.shield > 0:
            self.shield -= 1
            self.log('Shield\'s timer is now {}.'.format(self.shield))
        if self.recharge > 0:
            self.recharge -= 1
            self.player_mana += 101
            self.log('Recharge restores {} mana; its timer is now {}.'.format(101, self.recharge))

    def do_turn(self, action):
        self.log('Player turn (HP {}, Mana {}) v (Boss - {})'.format(self.player_hp, self.player_mana, self.enemy_hp))
        self.manage_effects()
        if self.enemy_hp <= 0:
            return
        self.cast_spell(action)
        if self.enemy_hp <= 0:
            return

        self.log('Boss turn (HP {}, Mana {}) v (Boss - {})'.format(self.player_hp, self.player_mana, self.enemy_hp))
        self.manage_effects()
        if self.enemy_hp <= 0:
            return

        armor = 7 if self.shield else 0
        dmg = max(1, self.enemy_damage - armor)
        self.player_hp -= dmg
        self.log('Boss deals {} damage.'.format(dmg))
        if self.player_hp <= 0:
            raise BadAction('Player died.')

        if self.hard_mode:
            self.player_hp -= 1
        if self.player_hp <= 0:
            raise BadAction('Player died.')

    def execute(self):
        while self.enemy_hp > 0:
            self.log(
                'Player turn (HP {}, Mana {}) v (Boss - {})'.format(self.player_hp, self.player_mana, self.enemy_hp)
            )
            command = input('Command?')
            self.do_turn(PlayerAction(int(command)))

    def log(self, s):
        # print(s)
        # self._log.append(s)
        pass
