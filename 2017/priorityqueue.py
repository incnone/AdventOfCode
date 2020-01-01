import itertools
import heapq


class PriorityQueue(object):
    def __init__(self):
        self.pq = []                               # list of entries arranged in a heap
        self.entry_finder = dict()                 # mapping of tasks to entries
        self.REMOVED = '<removed-task>'            # placeholder for a removed task
        self.counter = itertools.count()           # unique sequence count

    def __bool__(self):
        return bool(self.pq)

    def add_task(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def add_task_if_better(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        if task in self.entry_finder and self.entry_finder[task][0] <= priority:
            return
        self.add_task(task, priority=priority)

    def remove_task(self, task):
        """Mark an existing task as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        """Remove and return the lowest priority task. Raise KeyError if empty."""
        return self.pop_task_with_priority()[1]

    def pop_task_with_priority(self):
        """Remove and return the lowest priority task and its priority. Raise KeyError if empty."""
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')


# def djikstra_path(start_node, end_node, neighbor_fn):
#     """
#     Implements Djikstra's algorithm.
#
#     start: Node
#         Node should be a hashable type
#     neighbor_fn : Node --> List[(Node, int)]
#         This function should accept a node and give a list of its neighbors, together with the distances to those
#         neighbors.
#     """
#     # Djikstra's algorithm.
#     pq = PriorityQueue()
#     pq.add_task(start_node, priority=0)
#     while pq:
#         distance, next_node = pq.pop_task_with_priority()
#         if next_building.is_assembled():
#             return distance
#         for neighbor in next_building.get_legal_successors():
#             pq.add_task_if_better(neighbor, priority=distance+1)
