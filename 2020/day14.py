import textwrap
import re


def get_test_input() -> str:
    return textwrap.dedent("""\
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return s


def make_bitmasks(s: str):
    return int(s.replace('X', '1'), 2), int(s.replace('X', '0'), 2)


def part_1(s):
    bitmask_0 = 2**64 - 1
    bitmask_1 = 0
    mem = dict()

    mem_regex = re.compile(r'mem\[(?P<address>\d+)\] = (?P<val>\d+)')
    for line in s.splitlines():
        if line.startswith('mask'):
            val = line.split()[2].rstrip('\n')
            bitmask_0, bitmask_1 = make_bitmasks(val)
        elif line.startswith('mem'):
            regex_gd = mem_regex.match(line).groupdict()
            mem[regex_gd['address']] = (int(regex_gd['val']) | bitmask_1) & bitmask_0

    print('Part 1:', sum(mem.values()))


def part_2(s):
    # brute force
    bitmasks = []
    mem = dict()

    mem_regex = re.compile(r'mem\[(?P<address>\d+)\] = (?P<val>\d+)')
    for line in s.splitlines():
        if line.startswith('mask'):
            bitmasks.clear()
            val = line.split()[2].rstrip('\n')
            num_xs = val.count('X')
            for repl in range(0, 2**num_xs):
                new_val_str = ''
                repl_str = f'{repl:0{num_xs}b}'
                repl_idx = -1
                for c in val[::-1]:
                    if c == 'X':
                        new_val_str = repl_str[repl_idx] + new_val_str
                        repl_idx -= 1
                    elif c == '1':
                        new_val_str = c + new_val_str
                    elif c == '0':
                        new_val_str = 'X' + new_val_str
                bitmasks.append(make_bitmasks(new_val_str))
        elif line.startswith('mem'):
            regex_gd = mem_regex.match(line).groupdict()
            for bitmask in bitmasks:
                address = (int(regex_gd['address']) | bitmask[1]) & bitmask[0]
                mem[address] = int(regex_gd['val'])

    print('Part 2:', sum(mem.values()))


def main():
    data = read_input(day_number=14, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
