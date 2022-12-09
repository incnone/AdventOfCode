import textwrap
import heapq
import itertools

from typing import Tuple, List


def get_test_input() -> str:
    return textwrap.dedent("""\
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581""")


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
        data.append(list(int(x) for x in line))
    return data


def adj_nodes(node, path):
    nodes = []
    for node in [(node[0], node[1]-1), (node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]+1)]:
        if node not in path:
            nodes.append(node)
    return nodes


def find_shortest_path(data):
    nodes_to_search = [(0, (0, 0), [])]
    finished_nodes = set()
    width, height = len(data[0]), len(data)
    end_node = (width - 1, height - 1)

    while nodes_to_search:
        dist, node, path = heapq.heappop(nodes_to_search)
        if node == end_node:
            return dist
        if node in finished_nodes:
            continue

        finished_nodes.add(node)
        for adj_node in adj_nodes(node, path):
            if 0 <= adj_node[0] < width and 0 <= adj_node[1] < height and adj_node not in finished_nodes:
                newdist = dist + data[adj_node[1]][adj_node[0]]
                heapq.heappush(nodes_to_search, (newdist, adj_node, path + [node]))

    return None


def part_1(data):
    print(f'Part 1: {find_shortest_path(data)}')


def part_2(data):
    cell_width, cell_height = len(data[0]), len(data)
    width, height = 5*cell_width, 5*cell_height
    newdata = [[0 for _ in range(width)] for _ in range(height)]
    for x, y in itertools.product(range(width), range(height)):
        offset = x//cell_width + y//cell_height
        newdata[y][x] = (data[y % cell_height][x % cell_width] + offset - 1) % 9 + 1
    print(f'Part 2: {find_shortest_path(newdata)}')


def main():
    data = read_input(day_number=15, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
