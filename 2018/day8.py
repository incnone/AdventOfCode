from getinput import get_input
import itertools
import textwrap


class Node(object):
    def __init__(self, num_iter):
        num_children = next(num_iter)
        num_metadata = next(num_iter)
        self.children = []
        self.metadata = []
        for _ in range(num_children):
            self.children.append(Node(num_iter))
        for _ in range(num_metadata):
            self.metadata.append(next(num_iter))

    def sum_metadata(self):
        return sum(c.sum_metadata() for c in self.children) + sum(self.metadata)

    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(self.children[idx-1].value() for idx in self.metadata if idx-1 < len(self.children))


def parse_input(s: str):
    return list(int(x) for x in s.split())


def part_1(input_str: str):
    nums = parse_input(input_str)
    root_node = Node(iter(nums))
    return root_node.sum_metadata()


def part_2(input_str: str):
    nums = parse_input(input_str)
    root_node = Node(iter(nums))
    return root_node.value()


def test_input():
    return textwrap.dedent("""\
    """)


def main():
    input_str = get_input(8)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
