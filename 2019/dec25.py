from intcode import IntcodeProgram, ConsoleOutput
import textwrap


class ShipExplorerInput(object):
    _set_up_commands = textwrap.dedent("""\
    north
    take mug
    north
    take food ration
    south
    east
    north
    east
    take semiconductor
    west
    south
    west
    south
    east
    take ornament
    north
    take coin
    east
    take mutex
    west
    south
    east
    take candy cane
    west
    west
    south
    east
    take mouse
    south
    west
    """)

    def __init__(self):
        self.input_str = ShipExplorerInput._set_up_commands
        self.cursor = 0
        self.inventory = {
            'mug': 1,
            'food ration': 1,
            'semiconductor': 1,
            'ornament': 1,
            'coin': 1,
            'mutex': 1,
            'candy cane': 1,
            'mouse': 1,
        }
        for idx in range(2**8):
            self.make_inv_into(idx)
            self.input_str += 'west\n'

    def get_input(self):
        try:
            print(self.input_str[self.cursor], end="")
            return ord(self.input_str[self.cursor])
        finally:
            self.cursor += 1

    def make_inv_into(self, idx):
        for pwr, item in zip(range(8), self.inventory.keys()):
            if not (idx & 2**pwr) and self.inventory[item]:
                self.input_str += "drop {}\n".format(item)
                self.inventory[item] = 0
            elif (idx & 2**pwr) and not self.inventory[item]:
                self.input_str += 'take {}\n'.format(item)
                self.inventory[item] = 1


class IOHandlerS2C(ShipExplorerInput, ConsoleOutput):
    def __init__(self):
        ShipExplorerInput.__init__(self)
        ConsoleOutput.__init__(self, use_ascii=True)


def get_input():
    with open('input/dec25.txt', 'r') as file:
        for line in file:
            return line


def part_1(intcode_str):
    program = IntcodeProgram(intcode_str, io_handler=IOHandlerS2C())
    program.execute()


if __name__ == "__main__":
    the_intcode = get_input()
    part_1(the_intcode)
