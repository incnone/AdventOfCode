from getinput import get_input


class Output(object):
    def __init__(self, is_bot, num):
        self.is_bot = is_bot
        self.num = num


class Bot(object):
    def __init__(self):
        self.low = None
        self.high = None
        self.low_target = None
        self.high_target = None

    def grab(self, val):
        if self.low is None:
            self.low = val
        elif self.low <= val:
            self.high = val
        else:
            self.high = self.low
            self.low = val

    def run(self, bots, outputs):
        if self.low is None or self.high is None:
            return False

        # Pass low value
        if self.low_target.is_bot:
            bots[self.low_target.num].grab(self.low)
        else:
            outputs[self.low_target.num] = self.low

        # Pass high value
        if self.high_target.is_bot:
            bots[self.high_target.num].grab(self.high)
        else:
            outputs[self.high_target.num] = self.high

        self.low = self.high = None
        return True


class BotFactory(object):
    def __init__(self, values, bot_instrs):
        self.values = values
        self.bots = dict()
        self.outputs = dict()
        self.bot_comparer = None
        for bot_num, bot_instr in bot_instrs.items():
            new_bot = Bot()
            new_bot.low_target = bot_instr[0]
            new_bot.high_target = bot_instr[1]
            self.bots[bot_num] = new_bot

    def execute(self):
        for val, tar in self.values.items():
            self.bots[tar].grab(val)

        any_activated = True
        while any_activated:
            any_activated = False
            for bot_num, bot in self.bots.items():
                if bot.low == 17 and bot.high == 61:
                    self.bot_comparer = bot_num
                this_bot_active = bot.run(self.bots, self.outputs)
                any_activated = any_activated or this_bot_active


def parse_input(s):
    values = dict()
    bots = dict()
    for line in s.splitlines(keepends=False):
        words = line.split()
        if words[0] == 'value':
            values[int(words[1])] = int(words[-1])
        elif words[0] == 'bot':
            bots[int(words[1])] = \
                (
                    Output(words[5] == 'bot', int(words[6])),
                    Output(words[-2] == 'bot', int(words[-1]))
                )
    return values, bots


def part_1(vals, bots):
    factory = BotFactory(vals, bots)
    factory.execute()
    return factory.bot_comparer


def part_2(vals, bots):
    factory = BotFactory(vals, bots)
    factory.execute()
    prod = 1
    for idx in range(0, 3):
        prod *= factory.outputs[idx]
    return prod


if __name__ == "__main__":
    the_vals, the_bots = parse_input(get_input(10))

    print('Part 1:', part_1(the_vals, the_bots))
    print('Part 2:', part_2(the_vals, the_bots))
