from getinput import get_input
import itertools
import textwrap
import toposort
from priorityqueue import PriorityQueue


def parse_input(s: str):
    step_graph = dict()
    for line in s.splitlines(keepends=False):
        words = line.split()
        source, target = words[1], words[7]
        if source not in step_graph:
            step_graph[source] = []
        if target not in step_graph:
            step_graph[target] = []
        step_graph[source].append(target)
    return step_graph


def part_1(input_str: str):
    # input_str = test_input()
    digraph = parse_input(input_str)
    toposorted_nodes = toposort.toposort_sorted(digraph.keys(), child_fn=lambda n: digraph[n], priority_fn=lambda n: n)
    return ''.join(toposorted_nodes)


def part_2(input_str: str):
    # input_str = test_input()
    num_workers = 5

    def task_length(task):
        return ord(task) - ord('A') + 1 + 60

    children = parse_input(input_str)
    parents = dict()
    for n in children.keys():
        parents[n] = []

    for n in children.keys():
        for k in children[n]:
            parents[k].append(n)

    def get_next_task():
        available_tasks = list(ky for ky, val in parents.items() if not val)
        return min(available_tasks) if available_tasks else None

    def update_tasks():
        for p in workers:
            if p is not None:
                p[1] -= 1

    def remove_completed_tasks():
        for idx, p in enumerate(workers):
            if p is not None and p[1] == 0:
                workers[idx] = None
                for c in children[p[0]]:
                    parents[c].remove(p[0])

    workers = [None]*(num_workers + 1)
    second = -1
    while parents:
        second += 1

        # Assign tasks
        next_worker = min(idx for idx, t in enumerate(workers) if t is None)
        while next_worker != num_workers:
            next_task = get_next_task()
            if next_task is None:
                break
            workers[next_worker] = [next_task, task_length(next_task)]
            del parents[next_task]
            next_worker = min(idx for idx, t in enumerate(workers) if t is None)

        update_tasks()
        # print(second, workers)
        remove_completed_tasks()

    return second + max([0] + [p[1] for p in workers if p is not None]) + 1


def test_input():
    return textwrap.dedent("""\
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.""")


def main():
    input_str = get_input(7)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
