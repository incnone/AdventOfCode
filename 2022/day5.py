import textwrap
import re


def get_test_input() -> str:
    return textwrap.dedent("""\
        [D]    
    [N] [C]    
    [Z] [M] [P]
     1   2   3 
    
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    num_stacks = 9
    reading_crates = True
    crates = []
    instructions = []
    for _ in range(num_stacks):
        crates.append([])

    for line in s.splitlines(keepends=False):
        if reading_crates:
            if line.startswith(' 1 '):
                reading_crates = False
                continue
            else:
                for crate in range(num_stacks+1):
                    idx = 4*crate + 1
                    if idx < len(line) and line[idx] != ' ':
                        crates[crate].append(line[idx])
        else:
            regex = re.compile(r'move (?P<num>\d+) from (?P<src>\d+) to (?P<dest>\d+)')
            m = regex.match(line)
            if m is not None:
                int_dict = dict()
                for k, v in m.groupdict().items():
                    int_dict[k] = int(v)
                instructions.append(int_dict)

    real_crates = []
    for c in crates:
        real_crates.append(list(reversed(c)))
    return real_crates, instructions


def part_1(crates, instrs):
    for i in instrs:
        n = i['num']
        src = i['src'] - 1
        dest = i['dest'] - 1
        cs = crates[src][-n:]
        crates[dest] = crates[dest] + list(reversed(cs)).copy()
        crates[src] = crates[src][:-n]

    print(crates)
    s = ''.join([c[-1] for c in crates])
    print(f'Part 1: {s}')


def part_2(crates, instrs):
    for i in instrs:
        n = i['num']
        src = i['src'] - 1
        dest = i['dest'] - 1
        cs = crates[src][-n:]
        crates[dest] = crates[dest] + cs.copy()
        crates[src] = crates[src][:-n]

    print(crates)
    s = ''.join([c[-1] for c in crates])
    print(f'Part 2: {s}')


def main():
    data = read_input(day_number=5, test=False)
    #part_1(*data)
    part_2(*data)


if __name__ == "__main__":
    main()
