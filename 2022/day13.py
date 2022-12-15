import textwrap
import functools


def get_test_input() -> str:
    return textwrap.dedent("""\
    [1,1,3,1,1]
    [1,1,5,1,1]
    
    [[1],[2,3,4]]
    [[1],4]
    
    [9]
    [[8,7,6]]
    
    [[4,4],4,4]
    [[4,4],4,4,4]
    
    [7,7,7,7]
    [7,7,7]
    
    []
    [3]
    
    [[[]]]
    [[]]
    
    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [1,[2,[3,[4,[5,6,0]]]],8,9]""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def str2list_c(s, cursor=0):
    ans = []
    cursor += 1
    num = ''
    while cursor < len(s):
        if s[cursor] == '[':
            num = ''
            l, c = str2list_c(s, cursor)
            ans.append(l)
            cursor = c
            continue
        elif s[cursor] == ',':
            if num:
                ans.append(int(num))
            num = ''
        elif s[cursor] == ']':
            if num:
                ans.append(int(num))
            cursor += 1
            return ans, cursor
        else:
            num += s[cursor]
        cursor += 1

    # bad since we didn't hit a ']'
    return None, None


def str2list(s):
    return str2list_c(s, 0)[0]


def intlist_compare(a1, a2):
    if type(a1) is int and type(a2) is int:
        return a1 - a2

    if type(a1) is int:
        return intlist_compare([a1], a2)

    if type(a2) is int:
        return intlist_compare(a1, [a2])

    for x, y in zip(a1, a2):
        c = intlist_compare(x, y)
        if c != 0:
            return c

    return len(a1) - len(a2)


def parse_input(s: str):
    data = []
    for pair in s.split('\n\n'):
        data.append(tuple(str2list(s) for s in pair.splitlines(keepends=False)))
    return data


def part_1(data):
    sum_indices = 0
    for idx, p in enumerate(data):
        sum_indices += (idx+1) if (intlist_compare(*p) < 0) else 0
    print(f'Part 1: {sum_indices}')


def part_2(data):
    unpaired_data = []
    for p in data:
        unpaired_data.append(p[0])
        unpaired_data.append(p[1])
    unpaired_data.append([[2]])
    unpaired_data.append([[6]])

    unpaired_data.sort(key=functools.cmp_to_key(intlist_compare))
    idx_2, idx_6 = None, None
    for idx, a in enumerate(unpaired_data):
        if a == [[2]]:
            idx_2 = idx + 1
        elif a == [[6]]:
            idx_6 = idx + 1
    print(f'Part 2: {idx_2*idx_6}')


def main():
    data = read_input(day_number=13, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
