from priorityqueue import PriorityQueue


def toposort_sorted(nodes, child_fn, priority_fn):
    # Find all root nodes
    parents = dict()
    for n in nodes:
        parents[n] = []

    for n in nodes:
        for k in child_fn(n):
            parents[k].append(n)

    pq = PriorityQueue()
    for n, ps in parents.items():
        if not ps:
            pq.add_task(n, priority=priority_fn(n))

    toposorted_nodes = []
    while pq:
        n = pq.pop_task()
        toposorted_nodes.append(n)
        for c in child_fn(n):
            parents[c].remove(n)
            if not parents[c]:
                pq.add_task(c, priority=priority_fn(c))

    for n, ps in parents.items():
        if ps:
            raise ToposortNonacyclicError()

    return toposorted_nodes


def toposort(nodes, child_fn):
    def _toposort_visit(k):
        if k in visited_nodes:
            return
        if k in marked_nodes:
            raise ToposortNonacyclicError()
        marked_nodes.add(k)
        for m in child_fn(k):
            _toposort_visit(m)
        marked_nodes.remove(k)
        visited_nodes.add(k)
        toposorted_nodes.append(k)

    toposorted_nodes = []
    visited_nodes = set()
    marked_nodes = set()
    for n in nodes:
        if n not in marked_nodes:
            _toposort_visit(n)
    return list(reversed(toposorted_nodes))


class ToposortNonacyclicError(RuntimeError):
    def __init__(self):
        RuntimeError.__init__(self, 'Tried to toposort a graph with a cycle.')