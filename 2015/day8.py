from getinput import get_input


def parse_input(big_str):
    return list(big_str.splitlines(keepends=False))


def part_1(str_list):
    special_chars = 0
    for string in str_list:
        special_chars += 2
        skip = 0
        for s, t in zip(string[1:], string[2:]):
            if skip > 0:
                skip -= 1
                continue

            if s == '\\':
                if t == '"':
                    skip = 1
                    special_chars += 1
                elif t == '\\':
                    skip = 1
                    special_chars += 1
                elif t == 'x':
                    skip = 3
                    special_chars += 3

    return special_chars


def part_2(str_list):
    extra_chars = 0
    for string in str_list:
        extra_chars += 2
        for s in string:
            if s in ['"', '\\']:
                extra_chars += 1

    return extra_chars


if __name__ == "__main__":
    the_strings = parse_input(get_input(day=8))

    print('Part 1:', part_1(the_strings))
    print('Part 2:', part_2(the_strings))
