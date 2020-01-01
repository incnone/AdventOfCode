import unittest


def shortest_route(distances, start, end=None):
    """
    distances is a Dict[Tuple[str, str], int] whose keys are pairs of labelled verticies, and whose value at
    (x, y) is the distance from vertex x to vertex y.
    start is the string indicating the starting vertex
    """
    verticies = set(k[0] for k in distances.keys())
    best_paths = {(frozenset([start]), start): ((start,), 0)}
    for _ in range(len(verticies) - 1):
        this_iter_paths = dict()
        for state, path in best_paths.items():
            for v in verticies:
                if v not in state[0]:
                    new_state = (state[0].union([v]), v)
                    new_dist = path[1] + distances[(state[1], v)]
                    if new_state not in this_iter_paths or this_iter_paths[new_state][1] > new_dist:
                        new_path = path[0] + (v,)
                        this_iter_paths[new_state] = (new_path, new_dist)
        best_paths = this_iter_paths

    if end is not None:
        for state, path in best_paths.items():
            if state[1] == end:
                return path
    else:
        return min([path for state, path in best_paths.items()], key=lambda p: p[1])


def shortest_circuit(distances, start):
    """
    distances is a Dict[Tuple[str, str], int] whose keys are pairs of labelled verticies, and whose value at
    (x, y) is the distance from vertex x to vertex y.
    start is the string indicating the starting vertex
    """
    verticies = set(k[0] for k in distances.keys())
    best_paths = {(frozenset([start]), start): ((start,), 0)}
    for _ in range(len(verticies) - 1):
        this_iter_paths = dict()
        for state, path in best_paths.items():
            for v in verticies:
                if v not in state[0]:
                    new_state = (state[0].union([v]), v)
                    new_dist = path[1] + distances[(state[1], v)]
                    if new_state not in this_iter_paths or this_iter_paths[new_state][1] > new_dist:
                        new_path = path[0] + (v,)
                        this_iter_paths[new_state] = (new_path, new_dist)
        best_paths = this_iter_paths

    circuits = dict()
    for path in best_paths.values():
        circuits[path[0] + (start,)] = path[1] + distances[path[0][-1], start]
    return min(circuits.items(), key=lambda p: p[1])


class TestShortestRoute(unittest.TestCase):
    def test_shortest_route(self):
        import itertools
        distance_matrix = [
            [0, 1, 3, 4],
            [1, 0, 2, 5],
            [3, 2, 0, 9],
            [4, 5, 9, 0]
        ]
        distances = dict()
        for x, y in itertools.product(range(len(distance_matrix)), range(len(distance_matrix))):
            distances[(x, y)] = distance_matrix[y][x]

        self.assertEqual(((0, 2, 1, 3), 10), shortest_route(distances, 0))


if __name__ == "__main__":
    unittest.main()
