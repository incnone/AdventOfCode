import textwrap
import statistics


def get_test_input() -> str:
    return textwrap.dedent("""\
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]""")


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


def first_illegal_char(s: str):
    stack = []
    closers = {
        '{': '}',
        '[': ']',
        '(': ')',
        '<': '>',
    }
    for c in s:
        if c in closers.keys():
            stack.append(c)
        elif c in closers.values():
            desired = closers[stack[-1]]
            if c != desired:
                return c
            else:
                stack.pop(-1)
    return None


def desired_close(s: str):
    stack = []
    closers = {
        '{': '}',
        '[': ']',
        '(': ')',
        '<': '>',
    }
    for c in s:
        if c in closers.keys():
            stack.append(c)
        elif c in closers.values():
            desired = closers[stack[-1]]
            if c != desired:
                return None
            else:
                stack.pop(-1)

    return ''.join(closers[c] for c in reversed(stack))


def score_close_str(s: str):
    pts = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    tot = 0
    for c in s:
        tot = 5*tot + pts[c]
    return tot


def part_1(data):
    tot = 0
    for line in data:
        b = first_illegal_char(line)
        if b == ')':
            tot += 3
        elif b == ']':
            tot += 57
        elif b == '}':
            tot += 1197
        elif b == '>':
            tot += 25137
        else:
            pass
    print(f'Part 1: {tot}')


def part_2(data):
    data = [x for x in data if first_illegal_char(x) is None]
    scores = []
    for line in data:
        closer = desired_close(line)
        scores.append(score_close_str(closer))
        #print(line, closer, scores[-1])
    print(f'Part 2: {statistics.median(scores)}')


def main():
    data = read_input(day_number=10, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
