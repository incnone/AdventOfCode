import queue


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
