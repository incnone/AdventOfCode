from getinput import get_input
import itertools
import textwrap


class Ingredient(object):
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{} ({}, {}, {}, {}, {})'.format(
            self.name, self.capacity, self.durability, self.flavor, self.texture, self.calories
        )


def parse_ingredient_line(s):
    words = s.split()
    return Ingredient(
        name=words[0].rstrip(':'),
        capacity=int(words[2].rstrip(',')),
        durability=int(words[4].rstrip(',')),
        flavor=int(words[6].rstrip(',')),
        texture=int(words[8].rstrip(',')),
        calories=int(words[10].rstrip(','))
    )


def parse_input(big_str):
    ingredients = []
    for line in big_str.splitlines(keepends=False):
        ingredients.append(parse_ingredient_line(line))
    return ingredients


def part_1(ingredients):
    print(ingredients)
    teaspoons = 100
    max_score = -9999999
    max_ingrs = None
    for x in range(teaspoons+1):
        for y in range(teaspoons-x+1):
            for z in range(teaspoons-x-y+1):
                w = 100 - x - y - z
                ingrs = [x, y, z, w]
                cap = max(sum(i.capacity*amt for i, amt in zip(ingredients, ingrs)), 0)
                dur = max(sum(i.durability*amt for i, amt in zip(ingredients, ingrs)), 0)
                flav = max(sum(i.flavor*amt for i, amt in zip(ingredients, ingrs)), 0)
                text = max(sum(i.texture*amt for i, amt in zip(ingredients, ingrs)), 0)
                score = cap*dur*flav*text
                if score > max_score:
                    max_score = score
                    max_ingrs = ingrs
    return max_score


def part_2(ingredients):
    print(ingredients)
    teaspoons = 100
    max_score = -9999999
    max_ingrs = None
    for x in range(teaspoons+1):
        for y in range(teaspoons-x+1):
            for z in range(teaspoons-x-y+1):
                w = 100 - x - y - z
                ingrs = [x, y, z, w]
                cals = sum(i.calories*amt for i, amt in zip(ingredients, ingrs))
                if cals != 500:
                    continue

                cap = max(sum(i.capacity*amt for i, amt in zip(ingredients, ingrs)), 0)
                dur = max(sum(i.durability*amt for i, amt in zip(ingredients, ingrs)), 0)
                flav = max(sum(i.flavor*amt for i, amt in zip(ingredients, ingrs)), 0)
                text = max(sum(i.texture*amt for i, amt in zip(ingredients, ingrs)), 0)
                score = cap*dur*flav*text
                if score > max_score:
                    max_score = score
                    max_ingrs = ingrs
    return max_score


if __name__ == "__main__":
    the_ingredients = parse_input(get_input(day=15))

    print('Part 1:', part_1(the_ingredients))
    print('Part 2:', part_2(the_ingredients))
