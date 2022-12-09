import textwrap
import re


class Food(object):
    def __init__(self, rdict):
        self.ingredients = set(rdict['ingr'].split())
        self.allergens = set(x.rstrip(',') for x in rdict['alrg'].split())

    def __str__(self):
        return f'{" ".join(self.ingredients)} (contains {" ".join(self.allergens)})'


def get_test_input() -> str:
    return textwrap.dedent("""\
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    regex = re.compile(r'^(?P<ingr>.*) \(contains (?P<alrg>.*)\)$')
    data = []
    for line in s.splitlines(keepends=False):
        data.append(Food(regex.match(line).groupdict()))
    return data


def get_maybe_allergen_dict(data):
    all_allergens = {a for f in data for a in f.allergens}
    allergen_dict = dict()
    for allergen in all_allergens:
        allergen_dict[allergen] = set.intersection(*[f.ingredients for f in data if allergen in f.allergens])
    return allergen_dict


def part_1(data):
    allergen_dict = get_maybe_allergen_dict(data)

    maybe_allergens = set(v for a in allergen_dict.values() for v in a)
    no_allergens = set()
    for f in data:
        for i in f.ingredients:
            if i not in maybe_allergens:
                no_allergens.add(i)

    num_appear = 0
    for f in data:
        for i in f.ingredients:
            if i in no_allergens:
                num_appear += 1
    print('Part 1:', num_appear)


def part_2(data):
    allergen_dict = get_maybe_allergen_dict(data)
    solved_allergens = set()
    while len(solved_allergens) < len(allergen_dict):
        # Find a solvable unsolved allergen
        solvable_allergen = None
        known_ingr = None
        for a, ingrs in allergen_dict.items():
            if len(ingrs) == 1 and a not in solved_allergens:
                solvable_allergen = a
                known_ingr = ingrs.pop()
                break
        solved_allergens.add(solvable_allergen)

        new_allergen_dict = dict()
        for a, ingrs in allergen_dict.items():
            if a != solvable_allergen:
                new_allergen_dict[a] = set(x for x in ingrs if x != known_ingr)
            else:
                new_allergen_dict[a] = {known_ingr}
        allergen_dict = new_allergen_dict

    exact_allergens = dict()
    for a, ingrs in allergen_dict.items():
        exact_allergens[a] = ingrs.pop()
    exact_allergens = sorted([x for x in exact_allergens.items()], key=lambda x: x[0])
    print(','.join(v[1] for v in exact_allergens))


def main():
    data = read_input(day_number=21, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
