from getinput import get_input
from collections import defaultdict
from logicgate import LogicGate, toposort_logicgates


def parse_input(big_str):
    logic_gates = []
    for line in big_str.splitlines(keepends=False):
        logic_gates.append(LogicGate(line))
    return logic_gates


def part_1(logic_gates):
    logic_gates = list(toposort_logicgates(logic_gates))
    # print('\n'.join(str(g) for g in logic_gates))
    wires = defaultdict(lambda: None)
    wires['1'] = 1
    for gate in logic_gates:
        gate.execute(wires)
    return wires['a']


def part_2(logic_gates):
    logic_gates = list(toposort_logicgates(logic_gates))
    # print('\n'.join(str(g) for g in logic_gates))
    wires = defaultdict(lambda: None)
    wires['1'] = 1
    for gate in logic_gates:
        if gate.output == 'b':
            wires['b'] = 16076
        else:
            gate.execute(wires)
    return wires['a']


if __name__ == "__main__":
    the_logic_gates = parse_input(get_input(day=7))

    # test_input = textwrap.dedent("""\
    # x AND y -> d
    # 123 -> x
    # NOT x -> h
    # y RSHIFT 2 -> g
    # x OR y -> e
    # x LSHIFT 2 -> f
    # 456 -> y
    # NOT y -> i""")
    # the_logic_gates = parse_input(test_input)

    print('Part 1:', part_1(the_logic_gates))
    print('Part 2:', part_2(the_logic_gates))
