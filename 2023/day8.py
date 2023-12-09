import textwrap
import math


def get_test_input() -> str:
    # return textwrap.dedent("""\
    # LLR
    #
    # AAA = (BBB, BBB)
    # BBB = (AAA, ZZZ)
    # ZZZ = (ZZZ, ZZZ)""")

    return textwrap.dedent("""\
    LR
    
    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


class Node(object):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def __str__(self):
        return f'{self.name} = ({self.left.name}, {self.right.name})'


def parse_input(s: str):
    data = dict()
    nodes = []
    instrs = None
    for line in s.splitlines(keepends=False):
        if instrs is None:
            instrs = line
            continue
        if not line:
            continue

        node, _, left, right = line.split()
        left = left[1:-1]
        right = right[:-1]
        data[node] = Node(node)
        nodes.append((node, left, right))

    for node, left, right in nodes:
        data[node].left = data[left]
        data[node].right = data[right]
    return instrs, data


def part_1(instrs, data):
    curnode = data['AAA']
    endnode = data['ZZZ']
    steps = 0
    instrs_len = len(instrs)
    while curnode != endnode:
        next_instr = instrs[steps % instrs_len]
        if next_instr == 'L':
            curnode = curnode.left
        else:
            curnode = curnode.right
        steps += 1
    print(f'Part 1: {steps}')


def get_path_data(startnode, instrs, data):
    """returns cycle start, cycle length, list of endnodes"""
    curnode = startnode
    endnodes = []            # steps on which we hit endnodes
    visited = set()          # (visited node name, instruction index)
    first_visited = dict()   # (visited node name, instruction index) --> first visited step

    step = 0
    instr_idx = 0
    instrs_len = len(instrs)

    while (curnode, instr_idx) not in visited:
        visited.add((curnode, instr_idx))
        first_visited[(curnode, instr_idx)] = step
        if curnode.name[-1] == 'Z':
            endnodes.append(step)

        instr = instrs[instr_idx]
        step += 1
        instr_idx = step % instrs_len
        if instr == 'L':
            curnode = curnode.left
        else:
            curnode = curnode.right

    cycle_start = first_visited[(curnode, instr_idx)]
    cycle_len = step - cycle_start

    return cycle_start, cycle_len, endnodes


def inefficient_part2(instrs, data):
    """trying the horribly inefficient way"""
    curnodes = []
    nextnodes = []
    for nodename in data.keys():
        if nodename.endswith('A'):
            curnodes.append(data[nodename])

    steps = 0
    instrs_len = len(instrs)
    while any((n.name[-1] != 'Z') for n in curnodes):
        nextnodes.clear()
        next_instr = instrs[steps % instrs_len]
        if next_instr == 'L':
            for node in curnodes:
                nextnodes.append(node.left)
        else:
            for node in curnodes:
                nextnodes.append(node.right)
        steps += 1
        curnodes, nextnodes = nextnodes, curnodes

    print(f'Part 2: {steps}')


def part_2(instrs, data):
    startnodes = []
    for node in data.values():
        if node.name[-1] == 'A':
            startnodes.append(node)

    path_data = dict()
    for node in startnodes:
        path_data[node] = get_path_data(node, instrs, data)

    # By inspection, in practice all our things are on cycles, so we can do an easy thing
    cycle_lengths = list(pd[1] for _, pd in path_data.items())
    print(f'Part 2: {math.lcm(*cycle_lengths)}')


def main():
    instrs, data = read_input(day_number=8, test=False)
    #part_1(instrs, data)
    part_2(instrs, data)


if __name__ == "__main__":
    main()
