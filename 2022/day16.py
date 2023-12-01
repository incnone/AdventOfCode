import textwrap
import re


def get_test_input() -> str:
    return textwrap.dedent("""\
    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
    Valve CC has flow rate=2; tunnels lead to valves DD, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve FF has flow rate=0; tunnels lead to valves EE, GG
    Valve GG has flow rate=0; tunnels lead to valves FF, HH
    Valve HH has flow rate=22; tunnel leads to valve GG
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve JJ has flow rate=21; tunnel leads to valve II""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    flows = dict()
    tunnels = dict()
    regex = re.compile(r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)')
    for line in s.splitlines(keepends=False):
        m = regex.match(line)
        assert m is not None
        flows[m.group(1)] = int(m.group(2))
        tunnels[m.group(1)] = m.group(3).split(',')
    return flows, tunnels


def get_moves(s, flows, tunnels):
    loc, turn, pressure, flow = s[0:4]
    open_valves = s[4:]

    if open_valves[loc] ==



def part_1(flows_s, tunnels_s):
    print(flows_s)
    print(tunnels_s)
    valve_to_index = dict()
    index_to_valve = dict()
    flows = dict()
    tunnels = dict()

    for idx, k in enumerate(flows_s.keys()):
        valve_to_index[k] = idx
        index_to_valve[idx] = k

    print(valve_to_index)
    for k, v in flows_s.items():
        flows[valve_to_index[k]] = v

    for k, v in tunnels_s.items():
        tunnels[valve_to_index[k]] = list(valve_to_index[s.strip()] for s in v)

    openable_valves = list(k for k in flows.keys() if flows[k] > 0)
    print(len(openable_valves))

    # A state is a tuple:
    # t[0] is our current valve location,
    # t[1] is the turn,
    # t[2] is the current pressure,
    # t[3] is the current flow,
    # t[i+4] = 1 iff openable valve i is open




def part_2(flows, tunnels):
    pass


def main():
    flows, tunnels = read_input(day_number=16, test=True)
    part_1(flows, tunnels)
    part_2(flows, tunnels)


if __name__ == "__main__":
    main()
