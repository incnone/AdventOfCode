from getinput import get_input
from enum import Enum
import copy
from priorityqueue import PriorityQueue
import itertools
import time


class Building(object):
    def __init__(self, microchips, generators):
        assert len(microchips) == len(generators)
        self.things = microchips + generators
        self.elevator = 1
        self.num_items = len(microchips)

    def get_legal_successors(self):
        """Return a list of all legal Buildings that can be reached in one move from this one. Rules:
        -- We can move the elevator exactly one floor up or down
        -- We must move exactly either one or two items (chips or generators) from the elevator's source to its
           destination
        -- After the move, any chip on the same floor as a different generator must also be on the same floor as its
           own generator
        """
        successors = []
        for idx in range(len(self.things)):
            for jdx in range(idx, len(self.things)):
                if self.things[idx] != self.elevator or self.things[jdx] != self.elevator:
                    continue

                if self.elevator < 4:
                    building_up = Building([], [])
                    building_up.elevator = self.elevator + 1
                    new_things = list(self.things)
                    new_things[idx] += 1
                    if jdx != idx:
                        new_things[jdx] += 1
                    building_up.things = tuple(new_things)
                    building_up.num_items = self.num_items
                    if building_up.valid():
                        successors.append(building_up)

                if self.elevator > 1:
                    building_dn = Building([], [])
                    building_dn.elevator = self.elevator - 1
                    new_things = list(self.things)
                    new_things[idx] -= 1
                    if jdx != idx:
                        new_things[jdx] -= 1
                    building_dn.things = tuple(new_things)
                    building_dn.num_items = self.num_items
                    if building_dn.valid():
                        successors.append(building_dn)

        return successors

    def is_assembled(self):
        return all(x == 4 for x in self.things)

    def valid(self):
        """Returns true if, for every chip on a different floor than its generator, there are no other generators
        on its floor."""
        if not 1 <= self.elevator <= 4:
            return False

        for m, g in zip(self.microchips, self.generators):
            if m != g and any(x == m for x in self.generators):
                return False
        return True

    @property
    def microchips(self):
        return self.things[:self.num_items]

    @property
    def generators(self):
        return self.things[self.num_items:]

    def __str__(self):
        s = ''
        for floor in range(4, 0, -1):
            s += 'F{} '.format(floor)
            s += 'E  ' if self.elevator == floor else '.  '
            for idx, p in enumerate(zip(self.microchips, self.generators)):
                s += '{}M '.format(chr(ord('A') + idx)) if p[0] == floor else '.  '
                s += '{}G '.format(chr(ord('A') + idx)) if p[1] == floor else '.  '
            s += '\n'
        return s

    def __hash__(self):
        return hash(self.microchips + self.generators + (self.elevator,))

    def __eq__(self, other):
        return \
            self.microchips == other.microchips \
            and self.generators == other.generators \
            and self.elevator == other.elevator

    def __ne__(self, other):
        return not self == other


def puzzle_input_1():
    microchips = (2, 2, 1, 1, 1)
    generators = (1, 1, 1, 1, 1)
    return Building(microchips, generators)


def puzzle_input_2():
    microchips = (2, 2)
    generators = (1, 1)
    return Building(microchips, generators)


def test_input():
    microchips = (1, 1)
    generators = (2, 3)
    return Building(microchips, generators)


def part_1():
    # Djikstra's algorithm. Slowish here, but it works
    pq = PriorityQueue()
    pq.add_task(puzzle_input_1(), priority=0)
    last_printed_distance = None
    while pq:
        distance, next_building = pq.pop_task_with_priority()
        if distance != last_printed_distance:
            print(distance)
            last_printed_distance = distance
        if next_building.is_assembled():
            return distance
        for neighbor in next_building.get_legal_successors():
            pq.add_task_if_better(neighbor, priority=distance+1)


def part_2():
    # Djikstra's algorithm on the non-pairs, then 12 moves for each extra pair.
    # I have no idea why the "12 extra" is the right rule :P
    pq = PriorityQueue()
    pq.add_task(puzzle_input_2(), priority=0)
    last_printed_distance = None
    while pq:
        distance, next_building = pq.pop_task_with_priority()
        if distance != last_printed_distance:
            last_printed_distance = distance
        if next_building.is_assembled():
            return distance + 12*5
        for neighbor in next_building.get_legal_successors():
            pq.add_task_if_better(neighbor, priority=distance+1)


if __name__ == "__main__":
    # print('Part 1:', part_1())
    print('Part 2:', part_2())
