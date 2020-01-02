from getinput import get_input
import itertools
import textwrap


def part_1(input_str: str):
    num_recipes = int(input_str)
    # num_recipes = 2018
    recipes = [3, 7]
    elf_1 = 0
    elf_2 = 1
    while len(recipes) < num_recipes + 10:
        rec_1, rec_2 = recipes[elf_1], recipes[elf_2]
        new_recipe = rec_1 + rec_2
        if new_recipe >= 10:
            recipes.append(new_recipe//10)
        recipes.append(new_recipe % 10)
        elf_1 = (elf_1 + rec_1 + 1) % len(recipes)
        elf_2 = (elf_2 + rec_2 + 1) % len(recipes)
    return ''.join(str(x) for x in recipes[-10:])


def part_2(input_str: str):
    desired_str = input_str
    desired_end = [int(x) for x in desired_str]
    recipes = [3, 7]
    elf_1 = 0
    elf_2 = 1
    while recipes[-len(desired_end):] != desired_end:
        rec_1, rec_2 = recipes[elf_1], recipes[elf_2]
        new_recipe = rec_1 + rec_2
        if new_recipe >= 10:
            recipes.append(1)
            if recipes[-len(desired_end):] == desired_end:
                break
        recipes.append(new_recipe % 10)
        elf_1 = (elf_1 + rec_1 + 1) % len(recipes)
        elf_2 = (elf_2 + rec_2 + 1) % len(recipes)

    return len(recipes) - len(desired_str)


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(14)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
