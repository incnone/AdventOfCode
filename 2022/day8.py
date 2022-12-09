import textwrap
import numpy as np


def get_test_input() -> str:
    return textwrap.dedent("""\
    30373
    25512
    65332
    33549
    35390""")


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
        data.append([int(x) for x in line])

    return np.array(data, dtype=np.byte)


def get_top_vis(trees):
    vis = np.zeros(trees.shape, dtype=np.bool_)
    height = np.zeros(trees.shape, dtype=np.byte)

    for x in range(vis.shape[0]):
        vis[0, x] = True
        height[0, x] = trees[0, x]

    for y in range(1, vis.shape[1]):
        for x in range(vis.shape[0]):
            vis[y, x] = trees[y, x] > height[y-1, x]
            height[y, x] = max(trees[y, x], height[y-1, x])

    return vis


def scenic_score(trees, y, x):
    ss_up = 0
    ss_down = 0
    ss_left = 0
    ss_right = 0

    height = trees[y, x]
    for idx in range(y-1, -1, -1):
        ss_up += 1
        if trees[idx, x] >= height:
            break
    for idx in range(y+1, trees.shape[1]):
        ss_down += 1
        if trees[idx, x] >= height:
            break
    for jdx in range(x-1, -1, -1):
        ss_left += 1
        if trees[y, jdx] >= height:
            break
    for jdx in range(x+1, trees.shape[0]):
        ss_right += 1
        if trees[y, jdx] >= height:
            break
    return int(ss_up*ss_down*ss_left*ss_right)


def part_1(data):
    top_vis = get_top_vis(data)
    left_vis = np.rot90(get_top_vis(np.rot90(data, 1)), -1)
    right_vis = np.rot90(get_top_vis(np.rot90(data, -1)), 1)
    bottom_vis = np.flipud(get_top_vis(np.flipud(data)))

    vis = top_vis | left_vis | right_vis | bottom_vis
    print(f'Part 1: {vis.sum()}')


def part_2(data):
    scores = np.zeros(data.shape, dtype=np.int64)
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            scores[y, x] = scenic_score(data, y, x)
    print(f'Part 2: {scores.max()}')


def main():
    data = read_input(day_number=8, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
