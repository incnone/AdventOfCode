import textwrap
import numpy as np
import queue


def get_test_input() -> str:
    return textwrap.dedent("""\
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def get_elev(c):
    if c == 'S':
        return 0
    elif c == 'E':
        return ord('z') - ord('a')
    else:
        return ord(c) - ord('a')


def dijkstra(start, at_end, get_neighbors):
    """
    Parameters
    ----------
    start: The starting position. Type T. Must be hashable.
    at_end: Function T --> bool. Returns true if we're at an end square.
    get_neighbors: Function T --> List(Tuple[T, float]). Gives the neighbors of the input along with the cost to move.

    Returns
    -------
    List[T, float] giving the path from start to finish, along with distances along the path
    """
    pq = queue.PriorityQueue()
    pq.put_nowait((0, start))
    distances = {start: 0}
    prevnodes = dict()
    numloops = 0
    end = None

    while not pq.empty():
        numloops += 1
        dist, pos = pq.get_nowait()

        if at_end(pos):
            end = pos
            break

        if distances[pos] < dist:
            continue

        moves = get_neighbors(pos)
        for next_pos, cost in moves:
            if next_pos not in distances or (dist + cost) < distances[next_pos]:
                distances[next_pos] = dist + cost
                prevnodes[next_pos] = pos
                pq.put_nowait((dist + cost, next_pos))

    if end not in distances:
        return None

    currpos = end
    soln_path = [(end, distances[end])]
    while currpos != start and currpos in prevnodes:
        currpos = prevnodes[currpos]
        soln_path.append((currpos, distances[currpos]))

    soln_path = reversed(soln_path)
    return soln_path


def parse_input(s: str):
    data = []
    start, end = None, None
    for row, line in enumerate(s.splitlines(keepends=False)):
        if 'S' in line:
            start = (row, line.index('S'))
        if 'E' in line:
            end = (row, line.index('E'))
        data.append([get_elev(c) for c in line])

    return np.array(data), start, end


def get_neighbors_forward(node, elev):
    current_elev = elev[node]
    neighbors = []
    for disp in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        new_node = (node[0] + disp[0], node[1] + disp[1])
        if 0 <= new_node[0] < elev.shape[0] and 0 <= new_node[1] < elev.shape[1] and elev[new_node] - current_elev <= 1:
            neighbors.append((new_node, 1))
    return neighbors


def get_neighbors_backward(node, elev):
    current_elev = elev[node]
    neighbors = []
    for disp in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        new_node = (node[0] + disp[0], node[1] + disp[1])
        if 0 <= new_node[0] < elev.shape[0] and 0 <= new_node[1] < elev.shape[1] and current_elev - elev[new_node] <= 1:
            neighbors.append((new_node, 1))
    return neighbors


def part_1(elev, start, end):
    soln_path = list(dijkstra(start, lambda n: n == end, lambda n: get_neighbors_forward(n, elev)))
    print(f'Part 1: {soln_path[-1][1]}')


def part_2(elev, start, end):
    soln_path = list(dijkstra(end, lambda n: elev[n] == 0, lambda n: get_neighbors_backward(n, elev)))
    print(f'Part 2: {soln_path[-1][1]}')


def main():
    elev, start, end = read_input(day_number=12, test=False)
    part_1(elev, start, end)
    part_2(elev, start, end)


if __name__ == "__main__":
    main()
