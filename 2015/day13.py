from getinput import get_input
import itertools
import textwrap


def parse_happiness_string(s):
    words = s.split()
    return words[0], words[-1].rstrip('.'), int(words[3]) if words[2] == 'gain' else -int(words[3])


def parse_input(big_str):
    names = set()
    happiness_dict = dict()
    for line in big_str.splitlines(keepends=False):
        gainer, target, happiness = parse_happiness_string(line)
        happiness_dict[(gainer, target)] = happiness
        names.add(gainer)
    return names, happiness_dict


def best_happiness(names, happiness_dict):
    max_so_far = -9999999
    names = list(names)
    for perm in itertools.permutations(names[1:]):
        total_happiness = 0
        for a, b in itertools.chain(zip(perm, perm[1:]), [(perm[-1], names[0]), (names[0], perm[0])]):
            total_happiness += happiness_dict[(a, b)] + happiness_dict[(b, a)]
        if total_happiness > max_so_far:
            max_so_far = total_happiness

    return max_so_far


def part_1(names, happiness_dict):
    return best_happiness(names, happiness_dict)


def part_2(names, happiness_dict):
    for name in names:
        happiness_dict[('ME', name)] = 0
        happiness_dict[(name, 'ME')] = 0
    names.add('ME')
    return best_happiness(names, happiness_dict)


def test_input():
    return textwrap.dedent("""\
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.""")


if __name__ == "__main__":
    the_names, the_happiness_dict = parse_input(get_input(day=13))
    # the_names, the_happiness_dict = parse_input(test_input())

    print('Part 1:', part_1(the_names, the_happiness_dict))
    print('Part 2:', part_2(the_names, the_happiness_dict))
