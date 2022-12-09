import textwrap
import itertools


def get_test_input() -> str:
    return textwrap.dedent("""\
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0
    
    fold along y=7
    fold along x=5""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    pts = set()
    folds = []
    for line in s.splitlines(keepends=False):
        if line.startswith('fold'):
            axis, val = line.split()[2].split('=')
            folds.append((axis, int(val)))
        elif line:
            pts.add(tuple(int(x) for x in line.split(',')))
    return pts, folds


def fold(pts, fold_axis, fold_place):
    new_pts = set()
    if fold_axis == 'y':
        for pt in pts:
            if pt[1] > fold_place:
                new_pts.add((pt[0], 2*fold_place - pt[1]))
            else:
                new_pts.add(pt)
    elif fold_axis == 'x':
        for pt in pts:
            if pt[0] > fold_place:
                new_pts.add((2*fold_place - pt[0], pt[1]))
            else:
                new_pts.add(pt)
    return new_pts


def print_pts(pts, w, h):
    print('\n'.join(
        ''.join('#' if (x, y) in pts else '.' for x in range(w)) for y in range(h)
    ))


def part_1(pts, folds):
    first_fold = folds[0]
    new_pts = fold(pts, first_fold[0], first_fold[1])
    print(f'Part 1: {len(new_pts)}')


def part_2(pts, folds):
    for f in folds:
        pts = fold(pts, f[0], f[1])
    w = max(p[0] for p in pts)
    h = max(p[1] for p in pts)
    print_pts(pts, w+1, h+1)


def main():
    pts, folds = read_input(day_number=13, test=False)
    part_1(pts, folds)
    part_2(pts, folds)


if __name__ == "__main__":
    main()
