from typing import Dict, List, Set
from collections import defaultdict


class ReagentList(defaultdict):        # type: Dict[str, int]
    def __init__(self, input_str=''):
        defaultdict.__init__(self, lambda: 0)
        for item in input_str.split(','):
            data = item.split()
            if data:
                self[data[1]] = int(data[0])

    def __str__(self):
        return ', '.join(['{amt} {agent}'.format(amt=amt, agent=agent) for agent, amt in self.items()])


class Reaction(object):
    def __init__(self, product, amount, reagent_list):
        self.product = product
        self.amount = amount
        self.reagent_list = reagent_list        # type: ReagentList

    @staticmethod
    def from_str(s):
        x = s.split('=>')
        product_data = x[1].strip().split()
        return Reaction(product=product_data[1], amount=int(product_data[0]), reagent_list=ReagentList(x[0]))

    def __str__(self):
        return '{reagents} => {amt} {agent}'.format(
            reagents=str(self.reagent_list),
            agent=self.product,
            amt=self.amount
        )


class ReactionDict(dict):
    """A Dict[str, Reaction] giving the reaction producing each agent."""

    def __init__(self, reaction_list: List[Reaction]):
        dict.__init__(self)
        for r in reaction_list:
            self[r.product] = r

        # Topologically sort the agents in our reaction list
        self.toposorted_agents = None
        self.refresh_toposorted_agents()

    def refresh_toposorted_agents(self):
        self.toposorted_agents = []
        unmarked_nodes = set(self.keys())       # type: Set[str]
        tempmarked_nodes = set()                # type: Set[str]
        while unmarked_nodes:
            self._toposort_visit(next(iter(unmarked_nodes)), unmarked_nodes, tempmarked_nodes)
        self.toposorted_agents = list(reversed(self.toposorted_agents))

    def _toposort_visit(self, key, unmarked_nodes, tempmarked_nodes):
        if key not in unmarked_nodes and key not in tempmarked_nodes:
            return
        elif key in tempmarked_nodes:
            raise RuntimeError('Tried to Toposort a cyclic graph')

        unmarked_nodes.remove(key)
        tempmarked_nodes.add(key)
        for subagent in self[key].reagent_list.keys():
            self._toposort_visit(subagent, unmarked_nodes, tempmarked_nodes)
        tempmarked_nodes.remove(key)
        self.toposorted_agents.append(key)


def get_needed_ore(desired_outputs: ReagentList, reaction_dict: ReactionDict):
    if not desired_outputs:
        return 0

    if len(desired_outputs) == 1 and 'ORE' in desired_outputs:
        return desired_outputs['ORE']

    # Find "highest" agent in desired_outputs, turn it into reagents, modify desired_outputs, and recurse
    for primary_agent in reaction_dict.toposorted_agents:
        if primary_agent in desired_outputs.keys():
            amt_needed = desired_outputs[primary_agent]
            reaction_needed = reaction_dict[primary_agent]
            num_reactions = -(-amt_needed//reaction_needed.amount)      # ceiling division
            reagents_needed = reaction_needed.reagent_list

            new_desired_outputs = ReagentList()
            for agent in desired_outputs.keys():
                if agent != primary_agent:
                    new_desired_outputs[agent] = desired_outputs[agent]
            for agent in reagents_needed.keys():
                if agent not in new_desired_outputs:
                    new_desired_outputs[agent] = 0
                new_desired_outputs[agent] += reagents_needed[agent]*num_reactions

            return get_needed_ore(new_desired_outputs, reaction_dict)


def part_1(reaction_dict):
    return get_needed_ore(ReagentList('1 FUEL'), reaction_dict)


def part_2(reaction_dict):
    target_ore = 10**12

    minval = 10**6  # Can definitely produce this much fuel
    maxval = 10**7  # Definitely can't produce this much fuel
    minore = get_needed_ore(ReagentList('{} FUEL'.format(minval)), reaction_dict)
    maxore = get_needed_ore(ReagentList('{} FUEL'.format(maxval)), reaction_dict)

    assert minore <= target_ore < maxore

    while maxval - minval > 1:
        halfval = (maxval + minval)//2
        halfore = get_needed_ore(ReagentList('{} FUEL'.format(halfval)), reaction_dict)
        if halfore > target_ore:
            maxval = halfval
        elif halfore < target_ore:
            minval = halfval
        else:
            print(halfval)

    return minval


def get_reactions():
    reaction_list = []
    with open('input/dec14.txt', 'r') as file:
        for line in file:
            reaction_list.append(Reaction.from_str(line))
    return ReactionDict(reaction_list)


def get_test_reactions():
    reaction_list = []
    test_str = """157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
    for line in test_str.splitlines():
        reaction_list.append(Reaction.from_str(line))
    return ReactionDict(reaction_list)


if __name__ == "__main__":
    reactions = get_reactions()
    print('Part 1:', part_1(reactions))
    print('Part 2:', part_2(reactions))
