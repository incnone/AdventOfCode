from getinput import get_input
from util import grouper
import itertools
import textwrap


class AuntSue(object):
    def __init__(self, number, properties):
        self.number = number
        self.properties = properties


def parse_sue(s):
    words = s.split()
    properties = dict()
    for key, val in grouper(words[2:], 2):
        properties[key.rstrip(':')] = int(val.rstrip(','))
    return AuntSue(
        number=int(words[1].rstrip(':')),
        properties=properties
    )


def parse_input(big_str):
    list_of_sues = []
    for line in big_str.splitlines(keepends=False):
        list_of_sues.append(parse_sue(line))
    return list_of_sues


def part_1(sues):
    desired = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
    }

    for sue in sues:
        for key, val in sue.properties.items():
            if desired[key] != val:
                break
        else:
            return sue.number


def part_2(sues):
    exact = {
        'children': 3,
        'samoyeds': 2,
        'akitas': 0,
        'vizslas': 0,
        'cars': 2,
        'perfumes': 1,
    }
    sue_has_more = {
        'cats': 7,
        'trees': 3,
    }
    sue_has_less = {
        'pomeranians': 3,
        'goldfish': 5,
    }

    for sue in sues:
        for key, val in sue.properties.items():
            if key in exact and exact[key] != val:
                break
            if key in sue_has_more and sue_has_more[key] >= val:
                break
            if key in sue_has_less and sue_has_less[key] <= val:
                break
        else:
            return sue.number


if __name__ == "__main__":
    the_sue_list = parse_input(get_input(day=16))

    print('Part 1:', part_1(the_sue_list))
    print('Part 2:', part_2(the_sue_list))
