import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    """)


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(line)
    return data


def parse_program_vars(data):
    program_vars = []
    for group_idx in range(0, 14):
        program_vars.append(tuple(int(data[group_idx*18 + line_idx].split()[-1]) for line_idx in [4, 5, 15]))
    return program_vars


def run_program(inp, program_vars):
    z = 0
    for s, vs in zip(inp, program_vars):
        w = int(s)
        x = 1 if ((z % 26 + vs[1]) != w) else 0
        y = 25 * x + 1
        z = (z//vs[0]) * y + (y + w + vs[2]) * x
    return z


def run_program_once(w, z, a, b, c):
    if w == (z % 26) + b:
        return z // a
    else:
        return 26 * (z // a) + w + c


def part_1(data):
    program_vars = parse_program_vars(data)
    print(program_vars)

    for trial in range(9999999, 1111110, -1):
        trial_str = str(trial)
        assert(len(trial_str) == 7)
        z = 0
        s = ''
        trial_idx = 0
        failed = False
        for a, b, c in program_vars:
            if a == 1:
                s += trial_str[trial_idx]
                z = run_program_once(int(trial_str[trial_idx]), z, a, b, c)
                trial_idx += 1
            elif a == 26:
                w = (z % 26) + b
                if not 1 <= w <= 9:
                    failed = True
                    break
                s += str(w)
                z = run_program_once(w, z, a, b, c)
            else:
                assert False

        if not failed:
            print(f'Part 1: {s}')
            break


def part_2(data):
    program_vars = parse_program_vars(data)
    print(program_vars)

    for trial in range(1111111, 9999999, 1):
        trial_str = str(trial)
        assert(len(trial_str) == 7)
        z = 0
        s = ''
        trial_idx = 0
        failed = False
        for a, b, c in program_vars:
            if a == 1:
                new_digit = trial_str[trial_idx]
                if new_digit == '0':
                    failed = True
                    break
                s += new_digit
                z = run_program_once(int(new_digit), z, a, b, c)
                trial_idx += 1
            elif a == 26:
                w = (z % 26) + b
                if not 1 <= w <= 9:
                    failed = True
                    break
                s += str(w)
                z = run_program_once(w, z, a, b, c)
            else:
                assert False

        if not failed:
            print(f'Part 1: {s}')
            break


def main():
    data = read_input(day_number=24, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
