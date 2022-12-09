import textwrap
import functools


def get_test_input() -> str:
    return textwrap.dedent("""\
    C200B40A82
    04005AC33890
    880086C3E88112
    CE00C43D881120
    D8005AC2A8F0
    F600BC2D8F
    9C005AC2F8F0
    9C0141080250320F1802104A08""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


hex2bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


class Packet(object):
    def __init__(self, s: str, cursor=0):
        self.bits = ''.join(hex2bin[c] for c in s)
        self.cursor = cursor
        self.version = self._read_bits(3)
        self.type_id = self._read_bits(3)
        self.value = 0
        self.subpackets = []

        # literal value
        if self.type_id == 4:
            more_groups = True
            while more_groups:
                more_groups = bool(self._read_bits(1))
                self.value = self.value << 4
                self.value += self._read_bits(4)

        # operator
        else:
            # create subpackets
            length_type_id = self._read_bits(1)
            if length_type_id == 0:     # next 15 bits are total length in bits of subpackets
                bitlength_of_subpackets = self._read_bits(15)
                end_cursor = self.cursor + bitlength_of_subpackets
                while self.cursor < end_cursor:
                    self.subpackets.append(Packet(s, self.cursor))
                    self.cursor = self.subpackets[-1].cursor
            elif length_type_id == 1:   # next 11 bits is total number of subpackets
                number_of_subpackets = self._read_bits(11)
                for _ in range(number_of_subpackets):
                    self.subpackets.append(Packet(s, self.cursor))
                    self.cursor = self.subpackets[-1].cursor

            # compute value
            if self.type_id == 0:
                self.value = sum(self._subpacket_values())
            elif self.type_id == 1:
                self.value = functools.reduce((lambda x, y: x*y), self._subpacket_values(), 1)
            elif self.type_id == 2:
                self.value = min(self._subpacket_values())
            elif self.type_id == 3:
                self.value = max(self._subpacket_values())
            elif self.type_id == 5:
                self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
            elif self.type_id == 6:
                self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
            elif self.type_id == 7:
                self.value = 1 if self.subpackets[0].value == self.subpackets[1].value else 0

    def __repr__(self):
        return f'Packet: V{self.version}, T{self.type_id}, [{",".join(str(p) for p in self.subpackets)}]'

    def __str__(self):
        return f'Packet: V{self.version}, T{self.type_id}, [{",".join(str(p) for p in self.subpackets)}]'

    def _read_bits(self, n) -> int:
        ans = int(self.bits[self.cursor:self.cursor+n], 2)
        self.cursor += n
        return ans

    def _subpacket_values(self):
        return [p.value for p in self.subpackets]

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.subpackets)


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return data


def part_1(data):
    for line in data:
        packet = Packet(line)
        print(f'Part 1: {packet.version_sum()}')


def part_2(data):
    for line in data:
        packet = Packet(line)
        print(f'Part 2: {packet.value}')


def main():
    data = read_input(day_number=16, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
