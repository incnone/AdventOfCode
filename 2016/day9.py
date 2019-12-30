from getinput import get_input
import unittest


def decompress(s):
    decom = ''
    cursor = 0
    while cursor < len(s):
        if s[cursor] == '(':
            end_idx = s.find(')', cursor)
            params = s[cursor+1:end_idx].split('x')
            length = int(params[0])
            repeats = int(params[1])
            decom += s[end_idx+1:end_idx+1+length]*repeats
            cursor = end_idx + length + 1
        else:
            decom += s[cursor]
            cursor += 1
    return decom


def fully_decompressed_length(s):
    if not s:
        return 0

    if s[0] != '(':
        return 1 + fully_decompressed_length(s[1:])

    edx = s.find(')')
    params = s[1:edx].split('x')
    length = int(params[0])
    repeats = int(params[1])
    repeated_str = s[edx+1:edx+1+length]
    rest_of_str = s[edx+1+length:]
    return repeats*fully_decompressed_length(repeated_str) + fully_decompressed_length(rest_of_str)


def part_1(big_str):
    return len(decompress(big_str))


def part_2(big_str):
    return fully_decompressed_length(big_str)


class TestDecompress(unittest.TestCase):
    def test_decompress(self):
        tests = {
            "ADVENT": "ADVENT",
            "A(1x5)BC": "ABBBBBC",
            "(3x3)XYZ": "XYZXYZXYZ",
            "A(2x2)BCD(2x2)EFG": "ABCBCDEFEFG",
            "(6x1)(1x3)A": "(1x3)A",
            "X(8x2)(3x3)ABCY": "X(3x3)ABC(3x3)ABCY"
        }
        for k, v in tests.items():
            self.assertEqual(v, decompress(k))

    def test_decompress_v2(self):
        tests = {
            "ADVENT": 6,
            "A(1x5)BC": 7,
            "(3x3)XYZ": 9,
            "A(2x2)BCD(2x2)EFG": 11,
            "X(8x2)(3x3)ABCY": 20,
            "(27x12)(20x12)(13x14)(7x10)(1x12)A": 241920,
            "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN": 445
        }
        for k, v in tests.items():
            self.assertEqual(v, fully_decompressed_length(k), msg=k)


if __name__ == "__main__":
    # unittest.main()
    the_big_str = get_input(9)

    print('Part 1:', part_1(the_big_str))
    print('Part 2:', part_2(the_big_str))
