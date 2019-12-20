from getinput import get_input
import hashlib


def part_1(s):
    idx = 1
    while True:
        hash_str = hashlib.md5((s + str(idx)).encode('utf-8')).hexdigest()
        if hash_str[0:5] == '00000':
            break
        idx += 1
    return idx


def part_2(s):
    idx = 1
    while True:
        hash_str = hashlib.md5((s + str(idx)).encode('utf-8')).hexdigest()
        if hash_str[0:6] == '000000':
            break
        idx += 1
    return idx


if __name__ == "__main__":
    input_str = get_input(4)

    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))
