from getinput import get_input
import itertools
import textwrap
from collections import defaultdict
from typing import List, Tuple, Dict
import string


class Element(object):
    _idx = 0
    _name_to_element = dict()

    def __new__(cls, name):
        if str(name) in Element._name_to_element:
            return Element._name_to_element[name]
        else:
            new_element = super(Element, cls).__new__(cls)
            new_element.name = name
            new_element.idx = Element._idx
            Element._idx += 1
            Element._name_to_element[str(name)] = new_element
            return new_element

    def __hash__(self):
        return self.idx

    def __str__(self):
        return self.name

    def __repr__(self):
        return '[E]{}'.format(self.name)


class Molecule(object):
    @staticmethod
    def from_str(s):
        molecule = Molecule(tuple())
        skip = 0
        for c, d in itertools.zip_longest(s, s[1:], fillvalue=None):
            if skip:
                skip -= 1
                continue

            if d is not None and d in string.ascii_lowercase:
                element_name = c + d
                skip = 1
            else:
                element_name = c

            molecule.elements += (Element(element_name),)
        return molecule

    @property
    def length(self):
        return len(self.elements)

    def __init__(self, elements: Tuple[Element]):
        self.elements = elements

    def __hash__(self):
        return hash(self.elements)

    def __eq__(self, other):
        return self.elements == other.elements

    def __ne__(self, other):
        return self.elements != other.elements

    def __str__(self):
        return ''.join(str(e) for e in self.elements)

    def __repr__(self):
        return '[M]{}'.format(''.join(str(e) for e in self.elements))


class RecipeBook(object):
    def __init__(self):
        self.reaction_dict = defaultdict(lambda: [])
        self.molecules = defaultdict(lambda: [])            # type: Dict[Molecule, List[Element]]

    def add_recipe(self, element, recipe: Molecule):
        self.reaction_dict[element].append(recipe)
        self.molecules[recipe].append(element)

    def __getitem__(self, element) -> List[Molecule]:
        return self.reaction_dict[element]


def parse_input(big_str):
    recipe_book = RecipeBook()
    medicine_molecule = None
    for line in big_str.splitlines(keepends=False):
        parse_as_reaction = line.split(' => ')
        if len(parse_as_reaction) == 2:
            recipe_book.add_recipe(
                element=Element(parse_as_reaction[0]),
                recipe=Molecule.from_str(parse_as_reaction[1])
            )
        else:
            medicine_molecule = line

    return recipe_book, medicine_molecule


def find_all_children(recipe_book, mol, prune=lambda x: False):
    created_mols = set()

    for idx, el in enumerate(mol.elements):
        for recipe in recipe_book[el]:
            new_mol = Molecule(mol.elements[:idx] + recipe.elements + mol.elements[idx+1:])
            if not prune(new_mol):
                created_mols.add(new_mol)

    return created_mols


def find_all_parents(recipe_book: RecipeBook, mol: Molecule):
    electron = Element('e')
    parents = set()
    for res_mol in recipe_book.molecules.keys():
        if res_mol.length > mol.length:
            continue

        for idx in range(0, mol.length - res_mol.length + 1):
            if mol.elements[idx:idx+res_mol.length] == res_mol.elements:
                for elt in recipe_book.molecules[res_mol]:
                    if elt == electron:
                        if mol == res_mol:
                            parents.add(Molecule.from_str('e'))
                    else:
                        parents.add(Molecule(mol.elements[:idx] + (elt,) + mol.elements[idx+res_mol.length:]))
    return parents


def reduce(recipe_book: RecipeBook, mol: Molecule, start_idx=0):

    # Reduce all submolecules
    left_elt = Element('Rn')
    right_elt = Element('Ar')

    left_idx = start_idx
    while left_idx < mol.length and mol.elements[left_idx] != left_elt:
        left_idx += 1

    # If we don't have any submolecules, just directly reduce
    if left_idx == mol.length:
        steps = 0
        current_mols = {mol}
        reduced_mols = current_mols

        # Reduce the molecule we were given
        while current_mols:
            steps += 1
            next_mols = set()
            for mol in current_mols:
                next_mols = next_mols.union(find_all_parents(recipe_book, mol))
            reduced_mols = current_mols
            current_mols = next_mols

        return steps-1, reduced_mols

    # Otherwise, reduce the submolecule, then recurse on ourselves with proper replacements
    # Find the right bound
    right_idx = left_idx
    paren_depth = 0
    while right_idx < mol.length and paren_depth >= 0:
        right_idx += 1
        if mol.elements[right_idx] == left_elt:
            paren_depth += 1
        elif mol.elements[right_idx] == right_elt:
            paren_depth -= 1

    reduction_steps, submolecule_reductions = reduce(recipe_book, Molecule(mol.elements[left_idx+1:right_idx]))
    assert len(submolecule_reductions) == 1

    if reduction_steps == 0:
        return reduce(recipe_book, mol, start_idx=right_idx)

    for inner_reduction in submolecule_reductions:
        reduced_molecule = Molecule(mol.elements[:left_idx+1] + inner_reduction.elements + mol.elements[right_idx:])
        additional_steps, total_reduction = reduce(recipe_book, reduced_molecule)
        return additional_steps + reduction_steps, total_reduction


def part_1(recipe_book, medicine_mol_str):
    return len(find_all_children(recipe_book, Molecule.from_str(medicine_mol_str)))


def part_2(recipe_book, medicine_mol_str):
    mol = Molecule.from_str(medicine_mol_str)
    step, reduction = reduce(recipe_book, mol)
    return step


def test_input():
    return textwrap.dedent("""\
    e => H
    e => O
    H => HO
    H => OH
    O => HH

    HOHOHO""")


if __name__ == "__main__":
    test = False
    if not test:
        the_recipe_book, the_medicine_molecule = parse_input(get_input(day=19))
    else:
        the_recipe_book, the_medicine_molecule = parse_input(test_input())

    # print(reduce(the_recipe_book, Molecule.from_str('SiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgAr')))

    # print('Part 1:', part_1(the_recipe_book, the_medicine_molecule))
    print('Part 2:', part_2(the_recipe_book, the_medicine_molecule))
