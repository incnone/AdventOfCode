from getinput import get_input
import hashlib


def get_next_hash(base_str, start_int):
    while True:
        hash_str = base_str + str(start_int)
        hash_str = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
        if hash_str[0:5] == '00000':
            return start_int, hash_str
        start_int += 1


def part_1(base_str):
    password = ''
    start_int = 0
    for _ in range(8):
        start_int, next_hash = get_next_hash(base_str, start_int)
        password += next_hash[5]
        start_int += 1
    return password


def part_2(base_str):
    password = '........'
    start_int = 0
    valid_pos = set(range(8))
    while valid_pos:
        start_int, next_hash = get_next_hash(base_str, start_int)
        try:
            pos = int(next_hash[5])
        except ValueError:
            start_int += 1
            continue

        if pos not in valid_pos:
            start_int += 1
            continue

        valid_pos.remove(pos)
        password = password[:pos] + next_hash[6] + password[pos+1:]
        # print(password)
        start_int += 1
    return password


if __name__ == "__main__":
    the_input_str = get_input(5)

    print('Part 1:', part_1(the_input_str))
    print('Part 2:', part_2(the_input_str))
