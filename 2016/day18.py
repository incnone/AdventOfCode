from getinput import get_input


def parse_input(s):
    return [True if c == '^' else False for c in s]


def next_trap_row(s):
    next_row = [s[1]]
    next_row += [(s1 and not s2) or (not s1 and s2) for s1, s2 in zip(s, s[2:])]
    next_row += [s[-2]]
    return next_row


def generate_traps(init_row, num_rows):
    traps = [init_row]
    for _ in range(num_rows - 1):
        traps.append(next_trap_row(traps[-1]))
    return traps


def trap_str(traps):
    return '\n'.join(''.join('^' if c else '.' for c in line) for line in traps)


def part_1(trap_row):
    traps = generate_traps(trap_row, 40)
    return sum(sum(1 for x in line if not x) for line in traps)


def part_2(trap_row):
    traps = generate_traps(trap_row, 400000)
    return sum(sum(1 for x in line if not x) for line in traps)


if __name__ == "__main__":
    the_trap_list = parse_input(get_input(18))

    print('Part 1:', part_1(the_trap_list))
    print('Part 2:', part_2(the_trap_list))
