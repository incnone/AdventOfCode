import textwrap
from collections import defaultdict


def get_test_input() -> str:
    return textwrap.dedent("""\
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k""")


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
        data.append(line)
    return data


class Dir(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.subdirs = dict()   # dict (dirname, Dir)
        self.files = dict()         # name |-> size

    def get_str(self, indent=0):
        s = ' '*indent + f'- dir {self.name} (size {self.size})\n'
        for sd in self.subdirs.values():
            s += sd.get_str(indent=indent+2)
        for fname, sz in self.files.items():
            s += ' '*indent + f'  - {fname}: {sz}\n'
        return s

    @property
    def size(self):
        return sum(d.size for d in self.subdirs.values()) + sum(v for v in self.files.values())

    def part_1_size(self):
        ans = 0
        s = self.size
        if s <= 100000:
            ans += s
        ans += sum(d.part_1_size() for d in self.subdirs.values())
        return ans

    def add_recursively(self, lt):
        lt.append(self)
        for d in self.subdirs.values():
            d.add_recursively(lt)

    def __str__(self):
        return self.get_str(indent=0)


def make_dir_tree(data):
    root_dir = Dir(name='/', parent=None)
    working_dir = root_dir
    list_mode = False
    for cmd in data:
        args = cmd.split()
        if args[0] == '$':
            list_mode = False
            args = cmd.split()
            if args[1] == 'cd':
                dirname = args[2]
                if dirname == '/':
                    working_dir = root_dir
                elif dirname == '..':
                    if working_dir.parent is not None:
                        working_dir = working_dir.parent
                else:
                    if dirname not in working_dir.subdirs:
                        working_dir.subdirs[dirname] = Dir(name=dirname, parent=working_dir)
                    working_dir = working_dir.subdirs[dirname]
            elif args[1] == 'ls':
                list_mode = True
        elif list_mode:
            if args[0] == 'dir':
                working_dir.subdirs[args[1]] = Dir(name=args[1], parent=working_dir)
            else:
                working_dir.files[args[1]] = int(args[0])

    return root_dir


def part_1(data):
    root_dir = make_dir_tree(data)

    print(str(root_dir))
    print(f'Part 1: {root_dir.part_1_size()}')


def part_2(data):
    root_dir = make_dir_tree(data)
    all_dirs = []
    root_dir.add_recursively(all_dirs)

    total_space = 70000000
    needed_space = 30000000
    used_space = root_dir.size
    free_space = total_space - used_space
    delete_minimum = needed_space - free_space
    all_dirs = sorted(all_dirs, key=lambda d: d.size)
    for d in all_dirs:
        if d.size >= delete_minimum:
            print(f'Part 2: {d.size}')
            return


def main():
    data = read_input(day_number=7, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
