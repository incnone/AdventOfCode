from enum import Enum
from typing import Dict, List, Tuple, Callable, Optional, Set

import itertools
import string
import textwrap
import unittest

from pairs import Direction, add_pair, add_dir, dist_L1


class BlockType(Enum):
    WALL = 0
    GROUND = 1
    KEY = 2
    DOOR = 3


class Maze(object):
    @staticmethod
    def from_str(s: str):
        """
        '#' = Wall
        '.' = Empty ground
        '@' = Start location
        'a-z' = Key
        'A-Z' = Locked door
        """
        maze_data = []
        entrance = None
        keys = dict()
        doors = dict()
        for y, line in enumerate(s.splitlines()):
            maze_line = []
            for x, character in enumerate(line):
                if character == '#':
                    maze_line.append(BlockType.WALL)
                elif character == '.':
                    maze_line.append(BlockType.GROUND)
                elif character == '@':
                    maze_line.append(BlockType.GROUND)
                    entrance = (x, y)
                elif character in string.ascii_lowercase:
                    maze_line.append(BlockType.KEY)
                    keys[(x, y)] = character
                elif character in string.ascii_uppercase:
                    maze_line.append(BlockType.DOOR)
                    doors[(x, y)] = character.lower()
            maze_data.append(maze_line)

        return Maze(maze_data=maze_data, entrance=entrance, keys=keys, doors=doors)

    def __init__(self, maze_data, entrance, keys, doors):
        self.maze_data = maze_data
        self.entrance = entrance
        self.keys = keys
        self.doors = doors

    def __str__(self):
        return '\n'.join(self._strline(y) for y in range(len(self.maze_data)))

    def _strline(self, y: int) -> str:
        return ''.join(self._strchar(x, y) for x in range(len(self.maze_data[y])))

    def _strchar(self, x: int, y: int) -> str:
        tile_type = self.at((x, y))
        if tile_type == BlockType.GROUND:
            if (x, y) == self.entrance:
                return '@'
            else:
                return '.'
        elif tile_type == BlockType.WALL:
            return '#'
        elif tile_type == BlockType.KEY:
            return self.keys[(x, y)]
        elif tile_type == BlockType.DOOR:
            return self.doors[(x, y)].upper()
        raise RuntimeError('Maze._strchr({}, {}): Bad tile type {}'.format(x, y, tile_type))

    def at(self, loc: Tuple[int, int]) -> BlockType:
        return self.maze_data[loc[1]][loc[0]]

    def num_exits(self, loc: Tuple[int, int]) -> int:
        return len(self.exits(loc))

    def exits(self, loc: Tuple[int, int]) -> List[Direction]:
        if self.at(loc) == BlockType.WALL:
            raise RuntimeError('Called Maze.exits on a WALL tile, which is probably a mistake, so I crashed for you.')

        exits = []
        for direction in Direction:
            if self.at(add_dir(loc, direction)) != BlockType.WALL:
                exits.append(direction)
        return exits

    def _destroy_single_deadend(self, loc: Tuple[int, int]) -> None:
        while self.at(loc) == BlockType.GROUND and self.num_exits(loc) == 1:
            self.maze_data[loc[1]][loc[0]] = BlockType.WALL
            for direction in Direction:
                lookahead = add_dir(loc, direction)
                if self.at(lookahead) != BlockType.WALL:
                    loc = lookahead
                    break

    def destroy_deadends(self) -> None:
        deadends = set()
        for y, maze_row in enumerate(self.maze_data):
            for x, maze_tile in enumerate(maze_row):
                if maze_tile == BlockType.GROUND and self.num_exits((x, y)) == 1:
                    deadends.add((x, y))

        for x, y in deadends:
            self._destroy_single_deadend((x, y))

    def get_node_set(self) -> Set[Tuple[int, int]]:
        nodes = set()
        for y, maze_row in enumerate(self.maze_data):
            for x, maze_tile in enumerate(maze_row):
                tile_type = self.at((x, y))
                if (tile_type == BlockType.GROUND and self.num_exits((x, y)) > 2) \
                        or tile_type == BlockType.KEY or tile_type == BlockType.DOOR:
                    nodes.add((x, y))

        return nodes


class MazeNode(object):
    node_label = 0

    def __init__(self, loc, tile_type, dist, key_val=None):
        """
        exits: A list of paths out of this node
        """
        if key_val is None:
            key_val = str(MazeNode.node_label)
            MazeNode.node_label += 1

        self.loc = loc                  # type: Tuple[int, int]
        self.block_type = tile_type     # type: BlockType
        self.key_val = key_val          # type: str
        self.dist = dist                # type: int
        self.exits = []                 # type: List[MazeNode]

    def __hash__(self):
        return hash(self.loc)

    @property
    def type_char(self) -> str:
        if self.block_type == BlockType.WALL:
            return '#'
        elif self.block_type == BlockType.GROUND:
            return self.key_val
        elif self.block_type == BlockType.KEY:
            return self.key_val
        elif self.block_type == BlockType.DOOR:
            return self.key_val.upper()

    def get_keypaths(self):     # -> Dict[str, List[MazeNode]]:
        keypaths = dict()
        for node in self.exits:
            for keyval, path in node.get_keypaths().items():
                keypaths[keyval] = [self] + path

        if self.block_type == BlockType.KEY:
            keypaths[self.key_val] = [self]

        return keypaths

    def find_exits(self, maze: Maze, exit_dirs: List[Direction]):
        for direction in exit_dirs:
            # Go one step in this direction to see if there's a path to follow
            path_length = 1
            current_loc = add_dir(self.loc, direction)
            back_dir = direction.opposite
            if maze.at(current_loc) == BlockType.WALL:
                continue

            # There's a path to follow, so continue until we aren't on a straight path anymore
            exits = maze.exits(current_loc)
            while len(exits) == 2 and maze.at(current_loc) == BlockType.GROUND:
                for exit_dir in exits:
                    if exit_dir != back_dir:
                        current_loc = add_dir(current_loc, exit_dir)
                        back_dir = exit_dir.opposite
                        path_length += 1
                        break
                exits = maze.exits(current_loc)

            # If we've reached a deadend, don't log it
            current_tile_type = maze.at(current_loc)
            if len(exits) == 1 and current_tile_type == BlockType.GROUND:
                continue

            # If we are here, then we've found a new node we can connect to, so add it to our exits
            key_val = None
            if current_tile_type == BlockType.KEY:
                key_val = maze.keys[current_loc]
            elif current_tile_type == BlockType.DOOR:
                key_val = maze.doors[current_loc]
            new_node = MazeNode(loc=current_loc, tile_type=current_tile_type, dist=path_length, key_val=key_val)
            self.exits.append(new_node)

            # Find all exits for the new node
            new_exit_dirs = []
            for new_node_dirs in Direction:
                if new_node_dirs != back_dir:
                    new_exit_dirs.append(new_node_dirs)
            new_node.find_exits(maze, new_exit_dirs)


class MazeGraph(object):
    def __init__(self):
        self.entrance = None
        self.root_nodes = []    # type: List[MazeNode]
        self.keypaths = {}      # type: Dict[str, List[MazeNode]]

    @staticmethod
    def make(maze, entrance_offsets_and_outdirs: Dict[Tuple[int, int], List[Direction]]):
        maze_graph = MazeGraph()
        maze_graph.entrance = maze.entrance

        # Add the entrance nodes to our root nodes
        for offset in entrance_offsets_and_outdirs.keys():
            new_node = MazeNode(loc=add_pair(maze.entrance, offset), tile_type=BlockType.GROUND, dist=0)
            new_node.find_exits(maze=maze, exit_dirs=entrance_offsets_and_outdirs[offset])
            maze_graph.root_nodes.append(new_node)

        # Make keypaths
        for node in maze_graph.root_nodes:
            maze_graph.keypaths.update(node.get_keypaths())

        return maze_graph

    def key_dist(self, key_1, key_2):
        path_1 = self.keypaths[key_1]
        path_2 = self.keypaths[key_2]
        idx = 0
        while idx < min(len(path_1), len(path_2)) and path_1[idx] == path_2[idx]:
            idx += 1

        dist = 0
        if idx == 0:
            dist += dist_L1(path_1[0].loc, path_2[0].loc)

        return dist + sum(node.dist for node in itertools.chain(path_1[idx:], path_2[idx:]))

    def get_door_groups(self):
        """Assumes there are no duplicate doors"""
        door_groups = set()
        for key_path in self.keypaths.values():
            door_group = tuple()
            for node in key_path:
                if node.block_type == BlockType.DOOR:
                    door_group += (node.key_val,)
                else:
                    if len(door_group) > 1:
                        door_groups.add(door_group)
                    door_group = tuple()
        return door_groups

    def allowed_key_routes(self):
        """Too slow for lots of keys"""
        old_key_routes = [[]]
        placed_keys = set()
        for key_val, keypath in self.keypaths.items():
            new_key_routes = []
            key_requirements = set()
            for node in keypath:
                if node.block_type == BlockType.DOOR:
                    key_requirements.add(node.key_val.upper())

            for route in old_key_routes:
                needed_key = False
                requirements = key_requirements.copy()

                for idx, keychar in enumerate(route):

                    # If our key is required at this point in the route, replace the requirement and go to the next
                    # old route
                    if keychar == key_val.upper():
                        if not any((r.lower() in placed_keys) for r in requirements):
                            for still_needed in itertools.permutations(requirements):
                                new_key_routes.append(route[:idx] + list(still_needed) + [key_val] + route[idx+1:])
                        needed_key = True
                        break   # Go to the next old route, stop making extra permutations of this one

                    # Otherwise, if we haven't placed the remaining requirements, put our key in here with all
                    # requirements
                    if not any((r.lower() in placed_keys) for r in requirements):
                        for still_needed in itertools.permutations(requirements):
                            new_key_routes.append(
                                route[:idx] +
                                list(still_needed) +
                                [key_val] +
                                [k for k in route[idx:] if k != key_val.upper()]
                            )

                    # Take the current key out of the requirements
                    requirements.discard(keychar.upper())

                # Finally, append at the end, if we haven't placed the remaining requirements
                if not needed_key and not any((r.lower() in placed_keys) for r in requirements):
                    for still_needed in itertools.permutations(requirements):
                        new_key_routes.append(route + list(still_needed) + [key_val])

            placed_keys.add(key_val)
            old_key_routes = new_key_routes

        return old_key_routes

    def path_length(self, keys):
        last_key = keys[0]
        first_keypath = self.keypaths[last_key]
        path_length = dist_L1(self.entrance, first_keypath[0].loc)
        for node in first_keypath[1:]:
            path_length += node.dist
        for key_val in keys[1:]:
            path_length += self.key_dist(last_key, key_val)
            last_key = key_val
        return path_length

    @staticmethod
    def keypath_str(keypath):
        s = keypath[0].type_char
        for node in keypath[1:]:
            s += ' --{}--> {}'.format(node.dist, node.type_char)
        return s
        # return ' -> '.join(node.type_char for node in keypath)

    def __str__(self):
        to_follow = [(node, 1) for node in self.root_nodes]
        obtained_info = []
        while to_follow:
            node, depth = to_follow.pop(-1)
            obtained_info.append((node, depth))
            for exit_node in node.exits:
                to_follow.append((exit_node, depth+1))

        return '\n'.join(
            '{pathlen:.>{depth}} [{ty}]'.format(
                pathlen=node.dist,
                depth=depth,
                ty=node.type_char
            )
            for node, depth in obtained_info
        )


class TestMaze(unittest.TestCase):
    def test_import_export(self):
        testmaze = textwrap.dedent("""\
        #################
        #i.G..c...e..H.p#
        ########.########
        #j.A..b...f..D.o#
        ########@########
        #k.E..a...g..B.n#
        ########.########
        #l.F..d...h..C.m#
        #################""")

        maze = Maze.from_str(testmaze)
        self.assertEqual(testmaze, str(maze))

    def test_destroy_deadends(self):
        testmaze = textwrap.dedent("""\
        #################
        #...............#
        ########.########
        #j.A..b...f..D.o#
        ########@########
        #.....a......B.n#
        ########.########
        #..F..d...h..C.m#
        #################""")

        deadends_destroyed = textwrap.dedent("""\
        #################
        #################
        #################
        #j.A..b...f..D.o#
        ########@########
        ######a......B.n#
        ########.########
        ###F..d...h..C.m#
        #################""")

        maze = Maze.from_str(testmaze)
        maze.destroy_deadends()
        self.assertEqual(deadends_destroyed, str(maze))

    def test_get_node_set(self):
        testmaze = textwrap.dedent("""\
        #################
        #b.A..@....#.C.d#
        ########.###.####
        ###...a......B.c#
        #################""")

        maze = Maze.from_str(testmaze)
        expected_nodes = {
            (1, 1), (3, 1), (8, 1), (13, 1), (15, 1),
            (6, 3), (8, 3), (12, 3), (13, 3), (15, 3)
        }
        self.assertEqual(maze.get_node_set(), expected_nodes)

    def test_mazegraph(self):
        testmaze = textwrap.dedent("""\
        #################
        #b.A...@...#.C.d#
        ########.###.####
        ###..a.......B.c#
        #################""")

        desired = textwrap.dedent("""\
        0 [.]
        .3 [.]
        ..4 [.]
        ...1 [B]
        ....2 [c]
        ...3 [C]
        ....2 [d]
        ..3 [a]
        .4 [A]
        ..2 [b]""")

        maze = Maze.from_str(testmaze)
        maze.destroy_deadends()
        entrance_offsets = {(0, 0): [Direction.WEST, Direction.EAST]}
        maze_graph = MazeGraph.make(maze=maze, entrance_offsets_and_outdirs=entrance_offsets)
        self.assertEqual(desired, str(maze_graph))

        # Test keypaths
        desired_keypath_strs = ['. -> A -> b', '. -> . -> a', '. -> . -> . -> C -> d', '. -> . -> . -> B -> c']
        keypath_strs = []
        for key_val, keypath in maze_graph.keypaths.items():
            keypath_strs.append(' -> '.join(node.type_char for node in keypath))
        self.assertEqual(keypath_strs, desired_keypath_strs)

        # Test keydist
        keydists = [('a', 'b', 12), ('a', 'c', 10), ('a', 'd', 12), ('b', 'c', 16), ('b', 'd', 18), ('c', 'd', 8)]
        for k1, k2, d in keydists:
            self.assertEqual(d, maze_graph.key_dist(k1, k2))

    @unittest.skip
    def test_keyroutes(self):
        testmaze = textwrap.dedent("""\
        #################
        #b.A...@...#.C.d#
        ########.###.####
        #e.B.a.......B.c#
        #################""")
        maze = Maze.from_str(testmaze)
        maze.destroy_deadends()
        entrance_offsets = {(0, 0): [Direction.WEST, Direction.EAST]}
        maze_graph = MazeGraph.make(maze=maze, entrance_offsets_and_outdirs=entrance_offsets)

        # Test keyroutes
        self.assertCountEqual(
            [['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'e', 'd'], ['a', 'b', 'e', 'c', 'd']],
            maze_graph.allowed_key_routes()
        )

    def test_doorgroups(self):
        testmaze = textwrap.dedent("""\
        #################
        #c.B.A.@.e.#...d#
        ########.###b####
        #f.E.D.C.......a#
        #################""")
        maze = Maze.from_str(testmaze)
        maze.destroy_deadends()
        entrance_offsets = {(0, 0): [Direction.WEST, Direction.EAST]}
        maze_graph = MazeGraph.make(maze=maze, entrance_offsets_and_outdirs=entrance_offsets)

        self.assertCountEqual({('a', 'b'), ('c', 'd', 'e')}, maze_graph.get_door_groups())


if __name__ == "__main__":
    unittest.main()
