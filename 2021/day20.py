import textwrap
import itertools
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
    
    #..#.
    #....
    ##..#
    ..#..
    ..###""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    lines = s.splitlines(keepends=False)
    img_enh_alg = np.array([0 if c == '.' else 1 for c in lines[0]])
    img = np.array([[0 if c == '.' else 1 for c in line] for line in lines[2:]])

    return img_enh_alg, img


def extend(img: np.ndarray, val: int):
    new_img = np.zeros((img.shape[0] + 2*val, img.shape[1] + 2*val))
    new_img[val:-val, val:-val] = img
    return new_img


def get_indices_around(i, j):
    return [
        [i+1, j+1],
        [i+1, j],
        [i+1, j-1],
        [i, j+1],
        [i, j],
        [i, j-1],
        [i-1, j+1],
        [i-1, j],
        [i-1, j-1],
    ]


def enhance(alg, img):
    new_img = np.zeros(img.shape)
    for i, j in itertools.product(range(1, len(img)-1), range(1, len(img)-1)):
        b = int(sum((2**k)*img[x[0], x[1]] for k, x in enumerate(get_indices_around(i, j))))
        new_img[i, j] = alg[b]

    inf_char = img[0, 0]
    new_char = alg[0] if inf_char == 0 else alg[-1]
    for i, j in itertools.product([0, len(img)-1], range(len(img))):
        new_img[i, j] = new_char
    for i, j in itertools.product(range(len(img)), [0, len(img)-1]):
        new_img[i, j] = new_char

    return new_img


def show_img(img, newline=True):
    for line in img:
        print(''.join('.' if c == 0 else '#' for c in line))
    if newline:
        print()


def part_1(img_enh_alg, img):
    num_enhances = 2
    img = extend(img, num_enhances+2)
    for _ in range(num_enhances):
        img = enhance(img_enh_alg, img)
    print(f'Part 1: {int(sum(sum(row) for row in img))}')


def part_2(img_enh_alg, img):
    num_enhances = 50
    img = extend(img, num_enhances+2)
    for _ in range(num_enhances):
        img = enhance(img_enh_alg, img)
    print(f'Part 2: {int(sum(sum(row) for row in img))}')


def main():
    a, b = read_input(day_number=20, test=False)
    #part_1(a, b)
    part_2(a, b)


if __name__ == "__main__":
    main()
