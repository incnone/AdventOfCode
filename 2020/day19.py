import textwrap
import re
from typing import Dict


def get_test_input() -> str:
    return textwrap.dedent("""\
    42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: "a"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: "b"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1
    
    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    rules = dict()
    messages = []
    sections = s.split('\n\n')
    for line in sections[0].splitlines():
        rulenum, rule = line.split(':')
        rules[int(rulenum)] = rule.strip("\" ")
    for line in sections[1].splitlines():
        messages.append(line.rstrip('\n'))
    return rules, messages


def get_regex_str(rules: Dict[int, str], initial: int):
    reg_str = f'[{initial}]'
    rules_to_import = [initial]
    while rules_to_import:
        idx = rules_to_import.pop()
        rule = rules[idx]

        for v in rule.split():
            try:
                rules_to_import.append(int(v))
            except ValueError:
                pass

        format_rule = ''
        for v in rule.split():
            try:
                int(v)
                v = f'[{v}]'
            except ValueError:
                pass
            format_rule += v

        if '|' in format_rule:
            format_rule = f'({format_rule})'
        reg_str = reg_str.replace(f'[{str(idx)}]', format_rule)

    return reg_str


def part_1(rules, messages):
    regex = re.compile(f'^{get_regex_str(rules, 0)}$')
    print(str(regex))
    print('Part 1:', sum(1 if regex.match(msg) is not None else 0 for msg in messages))


def part_2(rules, messages):
    regex_42 = get_regex_str(rules, 42)
    regex_31 = get_regex_str(rules, 31)

    tot = 0
    matching_msgs = set()
    for m in range(1, 50):
        for n in range(1, m):
            new_regex = re.compile(f'^{regex_42}{{{m}}}{regex_31}{{{n}}}$')
            for msg in messages:
                if new_regex.match(msg) is not None:
                    matching_msgs.add(msg)
                    tot += 1

    print('Part 2:', tot)


def main():
    rules, messages = read_input(day_number=19, test=False)
    part_1(rules, messages)
    part_2(rules, messages)


if __name__ == "__main__":
    main()
