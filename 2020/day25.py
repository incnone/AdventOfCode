import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    5764801
    17807724""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.splitlines(keepends=False):
        data.append(int(line))
    return data


def get_loop_size(pubkey: int, subj_num=7) -> int:
    val = 1
    loops = 0
    while val != pubkey:
        loops += 1
        val = val*subj_num % 20201227
    return loops


def transform(pubkey: int, loop_size: int) -> int:
    val = 1
    for _ in range(loop_size):
        val = val * pubkey % 20201227
    return val


def part_1(data):
    card_pub_key, door_pub_key = data[0], data[1]
    card_loop = get_loop_size(card_pub_key)
    door_loop = get_loop_size(door_pub_key)
    print(transform(door_pub_key, card_loop))
    print(transform(card_pub_key, door_loop))


def part_2(data):
    pass


def main():
    data = read_input(day_number=25, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
