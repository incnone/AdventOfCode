from enum import Enum
from typing import Dict, List, Tuple, Callable, Optional, Set, FrozenSet

import itertools
import string
import textwrap
import unittest
import math

from pairs import Direction, add_pair, add_dir, dist_L1


class BlockType(Enum):
    WALL = 0
    GROUND = 1
    PORTAL = 2
    ENTRANCE = 3
    EXIT = 4
    NOTHING = 100


class Portal(object):
    portal_names = dict()
    name_idx = 0

    @staticmethod
    def short_name(portal_name):
        jdx = Portal.portal_names[portal_name]
        return string.ascii_letters[jdx]

    def __init__(self, name, exit_dir):
        self.name = name
        self.exit_dir = exit_dir

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        if name not in Portal.portal_names:
            Portal.portal_names[name] = Portal.name_idx
            Portal.name_idx += 1


class MazeTile(object):
    def __init__(self, tile_type, data=None):
        self.tile_type = tile_type
        self.data = data


class TorusMaze(object):
    @staticmethod
    def from_str(s: str):
        """
        '#' = Wall
        '.' = Empty ground
        '@' = Start location
        'AA-ZZ' = Portal
        """
        maze_data = dict()
        maze_str_data = s.splitlines()
        special_tiles = dict()

        for y, line in enumerate(maze_str_data):
            for x, character in enumerate(line):
                if character == '#':
                    maze_data[(x, y)] = MazeTile(BlockType.WALL)
                elif character == '.':
                    maze_data[(x, y)] = MazeTile(BlockType.GROUND)

                # Possible portal
                elif character in string.ascii_uppercase:
                    exit_dir = None

                    # Check if there's ground nearby, in which case we do make a portal/entrance/exit
                    for direction in Direction:
                        loc = add_dir((x, y), direction)
                        try:
                            if maze_str_data[loc[1]][loc[0]] == '.':
                                exit_dir = direction
                        except IndexError:
                            pass

                    # If we have a portal/entrance/exit, find the name
                    if exit_dir is not None:
                        portal_name = None
                        for direction in Direction:
                            loc = add_dir((x, y), direction)
                            try:
                                char_at_loc = maze_str_data[loc[1]][loc[0]]
                                if char_at_loc in string.ascii_uppercase:
                                    if direction == Direction.NORTH or direction == Direction.WEST:
                                        portal_name = char_at_loc+character
                                    else:
                                        portal_name = character+char_at_loc
                            except IndexError:
                                continue

                        special_tile_loc = add_dir((x, y), exit_dir)
                        if portal_name == 'AA':
                            special_tiles[special_tile_loc] = MazeTile(BlockType.ENTRANCE)
                        elif portal_name == 'ZZ':
                            special_tiles[special_tile_loc] = MazeTile(BlockType.EXIT)
                        else:
                            portal = Portal(name=portal_name, exit_dir=exit_dir)
                            special_tiles[special_tile_loc] = MazeTile(BlockType.PORTAL, data=portal)

        for loc, tile in special_tiles.items():
            maze_data[loc] = tile

        return TorusMaze(maze_data=maze_data)

    def __init__(self, maze_data):
        self.maze_data = maze_data      # type: Dict[Tuple[int, int], MazeTile]

    def __str__(self):
        bounds = self.bounds()
        return '\n'.join(self._strline(y, bounds[0:2]) for y in range(bounds[2], bounds[3]+1))

    def _strline(self, y: int, xbounds) -> str:
        return ''.join(self._strchar(x, y) for x in range(xbounds[0], xbounds[1]+1))

    def _strchar(self, x: int, y: int) -> str:
        tile = self.at((x, y))
        if tile.tile_type == BlockType.GROUND:
            return '.'
        elif tile.tile_type == BlockType.WALL:
            return '#'
        elif tile.tile_type == BlockType.PORTAL:
            return Portal.short_name(tile.data.name)
        elif tile.tile_type == BlockType.ENTRANCE:
            return '@'
        elif tile.tile_type == BlockType.EXIT:
            return '$'
        elif tile.tile_type == BlockType.NOTHING:
            return ' '
        raise RuntimeError('Maze._strchr({}, {}): Bad tile type {}'.format(x, y, tile.tile_type))

    def bounds(self):
        xmin = 99999999
        xmax = -99999999
        ymin = 99999999
        ymax = -99999999
        for loc in self.maze_data.keys():
            xmin = min(loc[0], xmin)
            xmax = max(loc[0], xmax)
            ymin = min(loc[1], ymin)
            ymax = max(loc[1], ymax)
        return xmin, xmax, ymin, ymax

    def at(self, loc: Tuple[int, int]) -> MazeTile:
        if loc in self.maze_data:
            return self.maze_data[loc]
        else:
            return MazeTile(BlockType.NOTHING)

    def num_exits(self, loc: Tuple[int, int]) -> int:
        return len(self.exits(loc))

    def exits(self, loc: Tuple[int, int]) -> List[Direction]:
        if self.at(loc).tile_type in [BlockType.WALL, BlockType.NOTHING]:
            raise RuntimeError('Called Maze.exits on a {} tile at ({}, {}), which is probably a mistake, so I '
                               'crashed for you.'.format(self.at(loc).tile_type, loc[0], loc[1]))

        exits = []
        for direction in Direction:
            if self.at(add_dir(loc, direction)).tile_type not in [BlockType.WALL, BlockType.NOTHING]:
                exits.append(direction)
        return exits

    def _destroy_single_deadend(self, loc: Tuple[int, int]) -> None:
        while self.at(loc).tile_type == BlockType.GROUND and self.num_exits(loc) == 1:
            self.maze_data[loc].tile_type = BlockType.WALL
            for direction in Direction:
                lookahead = add_dir(loc, direction)
                if self.at(lookahead).tile_type != BlockType.WALL:
                    loc = lookahead
                    break

    def destroy_deadends(self) -> None:
        deadends = set()
        for loc, maze_tile in self.maze_data.items():
            if maze_tile.tile_type == BlockType.GROUND and self.num_exits(loc) == 1:
                deadends.add(loc)

        for loc in deadends:
            self._destroy_single_deadend(loc)

    def get_exitportal_loc(self, portal_loc):
        # Find the portal
        portal = self.at(portal_loc)

        if portal.tile_type != BlockType.PORTAL:
            raise RuntimeError('TorusMaze.get_exitportal_loc({}, {}) called, but no portal at that location.'
                               .format(portal_loc[0], portal_loc[1]))

        for loc, maze_tile in self.maze_data.items():
            if maze_tile.tile_type == BlockType.PORTAL and maze_tile.data.name == portal.data.name\
                    and loc != portal_loc:
                return loc

        raise RuntimeError('TorusMaze.get_exitportal_loc({}, {}) called, but no exit portal found.'
                           .format(portal_loc[0], portal_loc[1]))


class MazeEdge(object):
    def __init__(self, source, target, length):
        self.source = source
        self.target = target
        self.length = length


class MazeNode(object):
    _global_node_label = 0

    def __init__(self, loc: Tuple[int, int], tile_type: BlockType, node_label=None):
        """
        exits: A list of paths out of this node
        """
        if node_label is None:
            node_label = str(MazeNode._global_node_label)
            MazeNode._global_node_label += 1

        self.exits = []                         # type: List[MazeEdge]

        self._loc = loc                         # type: Tuple[int, int]
        self._tile_type = tile_type             # type: BlockType
        self._node_label = node_label           # type: str

    def __hash__(self):
        return hash(self.loc)

    def __str__(self):
        return '({}, {}) --> [{}]'.format(
            self.loc[0],
            self.loc[1],
            '; '.join('{}: ({}, {})'.format(edge.length, edge.target.loc[0], edge.target.loc[1]) for edge in self.exits)
        )

    @property
    def loc(self):
        return self._loc

    @property
    def tile_type(self):
        return self._tile_type

    @property
    def node_label(self) -> str:
        return self._node_label


class TorusMazeGraph(object):
    def __init__(self):
        self.entrance = None        # type: Optional[MazeNode]

    @staticmethod
    def make(maze: TorusMaze):
        maze_graph = TorusMazeGraph()

        # Find the entrance (Portal 'AA') and create our root node
        for loc, maze_tile in maze.maze_data.items():
            if maze_tile.tile_type == BlockType.ENTRANCE:
                maze_graph.entrance = MazeNode(loc, BlockType.GROUND, '@')

        # Recursively fill out the graph
        checked_nodes = {maze_graph.entrance.loc: (maze_graph.entrance, False)}
        TorusMazeGraph._find_exits(maze_graph.entrance, maze, checked_nodes)

        return maze_graph

    @staticmethod
    def _find_exits(
            node: MazeNode,
            maze: TorusMaze,
            nodes: Dict[Tuple[int, int], Tuple[MazeNode, bool]]
    ):
        # If we've already checked this node, don't do it again
        if nodes[node.loc][1]:
            return

        for direction in Direction:
            # Go one step in this direction to see if there's a path to follow
            path_length = 1
            current_loc = add_dir(node.loc, direction)
            back_dir = direction.opposite
            if maze.at(current_loc).tile_type in [BlockType.WALL, BlockType.NOTHING]:
                continue

            # There's a path to follow, so continue until we aren't on a straight path anymore
            while True:
                # If we're on a portal, follow it and step onto the adjacent ground tile
                if maze.at(current_loc).tile_type == BlockType.PORTAL:
                    current_loc = maze.get_exitportal_loc(current_loc)
                    exitportal = maze.at(current_loc)
                    current_loc = add_dir(current_loc, exitportal.data.exit_dir)
                    back_dir = exitportal.data.exit_dir.opposite
                    path_length += 2
                    continue

                # Otherwise, we're on ground. If there isn't exactly one way to go forward, break out of the loop
                exits = maze.exits(current_loc)
                if len(exits) != 2:
                    break

                # There's exactly one way forward, so take it and log the way we came from
                for exit_dir in exits:
                    if exit_dir != back_dir:
                        current_loc = add_dir(current_loc, exit_dir)
                        back_dir = exit_dir.opposite
                        path_length += 1
                        break

            # If we've reached a deadend, don't log it
            current_tile = maze.at(current_loc)
            exits = maze.exits(current_loc)
            if len(exits) == 1 and current_tile.tile_type == BlockType.GROUND:
                continue

            # If we are here, then we've found a new node we can connect to, so add it to our exits
            if current_loc in nodes:
                new_node = nodes[current_loc][0]
            else:
                new_node = MazeNode(loc=current_loc, tile_type=current_tile.tile_type)
                nodes[new_node.loc] = (node, False)
            new_edge = MazeEdge(source=node, target=new_node, length=path_length)
            node.exits.append(new_edge)

            # Mark ourselves as completed so we don't loop on recurse
            nodes[node.loc] = (node, True)

            # Find all exits for the new node
            TorusMazeGraph._find_exits(new_node, maze, nodes)

    def all_nodes(self):
        all_nodes = set()
        if self.entrance is None:
            return all_nodes

        def _append_node(node):
            if node in all_nodes:
                return
            all_nodes.add(node)
            for exit_path in node.exits:
                _append_node(exit_path.target)

        _append_node(self.entrance)
        return all_nodes

    def shortest_path(self):
        # Slow implementation of Djikstra for now
        dist_to_entrance = dict()                   # type: Dict[MazeNode, float]

        def _append_node(node):
            if node in dist_to_entrance:
                return
            dist_to_entrance[node] = math.inf
            for exit_path in node.exits:
                _append_node(exit_path.target)

        _append_node(self.entrance)
        dist_to_entrance[self.entrance] = 0.0
        predecessor = {self.entrance: None}         # type: Dict[MazeNode, Optional[MazeNode]]
        nodes_to_check = set(dist_to_entrance.keys())

        while nodes_to_check:
            min_vertex = min(nodes_to_check, key=lambda node: dist_to_entrance[node])
            nodes_to_check.remove(min_vertex)
            for path_edge in min_vertex.exits:
                neighbor = path_edge.target
                if neighbor not in nodes_to_check:
                    continue
                new_dist = dist_to_entrance[min_vertex] + path_edge.length
                if new_dist < dist_to_entrance[neighbor]:
                    dist_to_entrance[neighbor] = new_dist
                    predecessor[neighbor] = min_vertex

        exit_node = None
        for node in dist_to_entrance.keys():
            if node.tile_type == BlockType.EXIT:
                exit_node = node
                break

        path = [exit_node]
        while path[-1] != self.entrance:
            path.append(predecessor[path[-1]])
        return dist_to_entrance[exit_node], reversed(path)

    def __str__(self):
        nodes_to_print = [self.entrance]
        nodes_printed = set()               # type: Set[Tuple[int,int]]
        s = ''
        while nodes_to_print:
            node = nodes_to_print.pop(-1)
            nodes_printed.add(node.loc)
            s += str(node) + '\n'
            for exit_path in node.exits:
                if exit_path.target.loc not in nodes_printed:
                    nodes_to_print.append(exit_path.target)
        return s.rstrip('\n')

    # def __str__(self):
    #     to_follow = [(self.entrance, 0, 0)]
    #     followed_already = set()    # type: Set[Tuple[int,int,int,int]]
    #     obtained_info = []
    #     while to_follow:
    #         node, depth, pathlen = to_follow.pop(-1)
    #         obtained_info.append((node, depth, pathlen))
    #         for exit_path in node.exits:
    #             follow_tuple = exit_path.source.loc + exit_path.target.loc
    #             if follow_tuple not in followed_already:
    #                 followed_already.add(follow_tuple)
    #                 to_follow.append((exit_path.target, depth+4, exit_path.length))
    #
    #     return '\n'.join(
    #         '{pathlen:.>{depth}} [{ty}]'.format(
    #             pathlen=pathlen,
    #             depth=depth,
    #             ty=node.node_label
    #         )
    #         for node, depth, pathlen in obtained_info
    #     )


class TestSimpleMaze(unittest.TestCase):
    def setUp(self) -> None:
        self.maze_str = textwrap.dedent("""\
                 A           
                 A           
          #######.#########  
          #.#.............#  
          #.#####.###.###.#  
          #.#.....###...#.#  
          #...###.#####.#.#  
          #####  B    #.#.#  
        BC...##  C    ###.#  
          ##.##       #.#.#  
          ##...DE  F  #.#.#  
          #####    G  #.#.#  
          ###.#####.###...#  
        DE..#.....#...###.#  
          #.##.#.####.###.#  
        FG..#..#..........#  
          ###########.#####  
                     Z       
                     Z     """)
        self.maze = TorusMaze.from_str(self.maze_str)

    def test_import_export(self):
        desired = textwrap.dedent("""\
         #######@#########
         #.#.............#
         #.#####.###.###.#
         #.#.....###...#.#
         #...###a#####.#.#
         #####       #.#.#
         a..##       ###.#
         ##.##       #.#.#
         ##..b       #.#.#
         #####       #.#.#
         ###.#####c###...#
         b.#.....#...###.#
         #.##.#.####.###.#
         c.#..#..........#
         ###########$#####""")

        self.assertEqual(desired, str(self.maze))


class TestNoDeadendsMaze(unittest.TestCase):
    def setUp(self) -> None:
        self.maze_str = textwrap.dedent("""\
                 A           
                 A           
          #######.#########  
          #.#.............#  
          #.#####.###.###.#  
          #.#.....###...#.#  
          #...###.#####.#.#  
          #####  B    #.#.#  
        BC...##  C    ###.#  
          ##.##       #.#.#  
          ##...DE  F  #.#.#  
          #####    G  #.#.#  
          ###.#####.###...#  
        DE..#.....#...###.#  
          #.##.#.####.###.#  
        FG..#..#..........#  
          ###########.#####  
                     Z       
                     Z     """)
        self.maze = TorusMaze.from_str(self.maze_str)
        self.maze.destroy_deadends()
        self.maze_graph = TorusMazeGraph.make(maze=self.maze)

    def test_destroy_deadends(self):
        desired = textwrap.dedent("""\
         #######@#########
         #######.........#
         #######.#######.#
         #######.#######.#
         #######a#######.#
         #####       ###.#
         a..##       ###.#
         ##.##       ###.#
         ##..b       ###.#
         #####       ###.#
         #########c#####.#
         b.#######...###.#
         #.#########.###.#
         c.#########.....#
         ###########$#####""")

        self.assertEqual(desired, str(self.maze))

    def test_mazegraph(self):
        desired = textwrap.dedent("""\
        (9, 2) --> [1: (9, 3)]
        (9, 3) --> [1: (9, 2); 21: (13, 15); 24: (13, 15)]
        (13, 15) --> [21: (9, 3); 1: (13, 16); 24: (9, 3)]
        (13, 16) --> [1: (13, 15)]
        (13, 15) --> [21: (9, 3); 1: (13, 16); 24: (9, 3)]""")

        self.assertEqual(desired, str(self.maze_graph))

    def test_shortest_path(self):
        desired = textwrap.dedent("""\
        (9, 2), (9, 3), (13, 15), (13, 16)""")

        length, shortest_path = self.maze_graph.shortest_path()
        length = int(length)
        path_str = ', '.join('({}, {})'.format(node.loc[0], node.loc[1]) for node in shortest_path)
        self.assertEqual(23, length)
        self.assertEqual(desired, path_str)


if __name__ == "__main__":
    unittest.main()
