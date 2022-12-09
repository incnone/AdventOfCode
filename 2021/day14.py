import textwrap
from collections import Counter, defaultdict


def get_test_input() -> str:
    return textwrap.dedent("""\
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    lines = s.splitlines(keepends=False)
    data.append(lines[0])
    rules = dict()
    for line in lines[2:]:
        words = line.split(' -> ')
        rules[words[0]] = words[1]
    data.append(rules)
    return data


def grow_polymer(base, rules):
    new_poly = base[0]
    for c1, c2 in zip(base, base[1:]):
        pair = ''.join([c1, c2])
        if pair in rules:
            new_poly += rules[pair]
        new_poly += c2
    return new_poly


def part_1(data):
    base, rules = data
    for _ in range(10):
        base = grow_polymer(base, rules)
    ctr = Counter(base)
    ctr = sorted(ctr.items(), key=lambda x: x[1])
    print(f'Part 1: {ctr[-1][1] - ctr[0][1]} ({ctr[-1][0]} - {ctr[0][0]})')


def part_2(data):
    base, rules = data
    pairs = defaultdict(lambda: 0)
    for c1, c2 in zip(base, base[1:]):
        pairs[''.join([c1, c2])] += 1
    print(pairs)

    def dostep(pairdict):
        newpairs = defaultdict(lambda: 0)
        for ky, vl in pairdict.items():
            n = rules[ky]
            newpairs[ky[0] + n] += vl
            newpairs[n + ky[1]] += vl
        return newpairs

    for _ in range(40):
        pairs = dostep(pairs)

    letters = defaultdict(lambda: 0)
    for k, v in pairs.items():
        letters[k[0]] += v
        letters[k[1]] += v

    letters[base[0]] += 1
    letters[base[-1]] += 1
    for k in letters.keys():
        letters[k] = letters[k] // 2

    ctr = sorted(letters.items(), key=lambda x: x[1])
    print(f'Part 2: {ctr[-1][1] - ctr[0][1]} ({ctr[-1][0]} - {ctr[0][0]})')


def main():
    data = read_input(day_number=14, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
