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

    ENTRANCE = 10
    EXIT = 11
    PORTAL = 12

    NOTHING = 100


class Portal(object):
    portal_names = dict()
    name_idx = 0

    @staticmethod
    def short_name(portal):
        jdx = Portal.portal_names[portal.name]
        try:
            return string.ascii_lowercase[jdx] if not portal.is_inward else string.ascii_uppercase[jdx]
        except IndexError:
            return '%'

    def __init__(self, name, exit_dir, is_inward):
        self.name = name
        self.exit_dir = exit_dir
        self.is_inward = is_inward

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


class FractalMaze(object):
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
                            # Figure out whether this portal is on the inside or outside
                            outward = x < 2 or x > len(maze_str_data[2]) - 3 or y < 2 or y > len(maze_str_data) - 3
                            portal = Portal(
                                name=portal_name,
                                exit_dir=exit_dir,
                                is_inward=not outward
                            )
                            special_tiles[special_tile_loc] = MazeTile(BlockType.PORTAL, data=portal)

        for loc, tile in special_tiles.items():
            maze_data[loc] = tile

        return FractalMaze(maze_data=maze_data)

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
            return Portal.short_name(tile.data)
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
                if self.at(lookahead).tile_type == BlockType.GROUND:
                    loc = lookahead
                    break

    def destroy_deadends(self) -> None:
        deadends = set()
        for loc, maze_tile in self.maze_data.items():
            if maze_tile.tile_type == BlockType.GROUND and self.num_exits(loc) == 1:
                deadends.add(loc)

        for loc in deadends:
            self._destroy_single_deadend(loc)

    def get_exitportal(self, portal_loc) -> Tuple[Tuple[int,int], MazeTile]:
        # Find the portal
        portal = self.at(portal_loc)

        if portal.tile_type != BlockType.PORTAL:
            raise RuntimeError('FractalMaze.get_exitportal_loc({}, {}) called, but no portal at that location.'
                               .format(portal_loc[0], portal_loc[1]))

        for loc, maze_tile in self.maze_data.items():
            if maze_tile.tile_type == BlockType.PORTAL and maze_tile.data.name == portal.data.name\
                    and loc != portal_loc:
                return loc, maze_tile

        raise RuntimeError('FractalMaze.get_exitportal_loc({}, {}) called, but no exit portal found.'
                           .format(portal_loc[0], portal_loc[1]))


class MazeEdge(object):
    def __init__(self, source, target, length, depth_increment):
        self.source = source
        self.target = target
        self.length = length
        self.depth_increment = depth_increment


class MazeNode(object):
    _global_node_label = 0

    def __init__(self, loc: Tuple[int, int], tile_type, node_label=None):
        """
        exits: A list of paths out of this node
        """
        if node_label is None:
            node_label = str(MazeNode._global_node_label)
            MazeNode._global_node_label += 1

        self.exits = []                         # type: List[MazeEdge]

        self._loc = loc                         # type: Tuple[int, int]
        self._node_label = node_label           # type: str
        self._tile_type = tile_type

    def __hash__(self):
        return hash(self.loc)

    def __str__(self):
        return '({}, {}) --> [{}]'.format(
            self.loc[0],
            self.loc[1],
            '; '.join('{}: ({}, {})'.format(edge.length, edge.target.loc[0], edge.target.loc[1]) for edge in self.exits)
        )

    def __eq__(self, other):
        return self.loc == other.loc

    def __ne__(self, other):
        return self.loc != other.loc

    @property
    def loc(self):
        return self._loc

    @property
    def node_label(self) -> str:
        return self._node_label

    @property
    def tile_type(self) -> str:
        return self._tile_type


class FractalMazeGraph(object):
    def __init__(self):
        self.entrance = None        # type: Optional[MazeNode]

    @staticmethod
    def make(maze: FractalMaze):
        maze_graph = FractalMazeGraph()

        # Find the entrance (Portal 'AA') and create our root node
        for loc, maze_tile in maze.maze_data.items():
            if maze_tile.tile_type == BlockType.ENTRANCE:
                maze_graph.entrance = MazeNode(loc, '@')

        # Recursively fill out the graph
        checked_nodes = {maze_graph.entrance.loc: (maze_graph.entrance, False)}
        FractalMazeGraph._find_exits(maze_graph.entrance, maze, checked_nodes)

        return maze_graph

    @staticmethod
    def _make_path_and_find_new_exits(
            source_node: MazeNode,
            target_loc: Tuple[int, int],
            path_length: int,
            depth_increment: int,
            nodes: Dict[Tuple[int, int], Tuple[MazeNode, bool]],
            maze: FractalMaze
    ):
        if target_loc in nodes:
            target_node = nodes[target_loc][0]
        else:
            target_node = MazeNode(loc=target_loc, tile_type=maze.at(target_loc).tile_type)
            nodes[target_loc] = (target_node, False)

        new_edge = MazeEdge(source=source_node, target=target_node, length=path_length, depth_increment=depth_increment)
        source_node.exits.append(new_edge)
        FractalMazeGraph._find_exits(target_node, maze, nodes)

    @staticmethod
    def _find_exits(
            node: MazeNode,
            maze: FractalMaze,
            nodes: Dict[Tuple[int, int], Tuple[MazeNode, bool]]
    ):
        # If we've already checked this node, don't do it again
        if nodes[node.loc][1]:
            return

        # Mark ourselves as completed so we don't loop on recurse
        nodes[node.loc] = (node, True)

        # If we're on a portal, create a path to the corresponding portal
        if maze.at(node.loc).tile_type == BlockType.PORTAL:
            exitportal_loc, exitportal = maze.get_exitportal(node.loc)
            FractalMazeGraph._make_path_and_find_new_exits(
                source_node=node,
                target_loc=exitportal_loc,
                path_length=1,
                nodes=nodes,
                depth_increment=-1 if exitportal.data.is_inward else 1,
                maze=maze
            )

        # Check all walkable paths
        for direction in Direction:
            # Go one step in this direction to see if there's a path to follow
            path_length = 1
            current_loc = add_dir(node.loc, direction)
            back_dir = direction.opposite
            if maze.at(current_loc).tile_type in [BlockType.WALL, BlockType.NOTHING]:
                continue

            # There's a path to follow, so continue until we aren't on a straight path anymore
            exits = maze.exits(current_loc)
            while len(exits) == 2:
                # There's exactly one way forward, so take it and log the way we came from
                for exit_dir in exits:
                    if exit_dir != back_dir:
                        current_loc = add_dir(current_loc, exit_dir)
                        back_dir = exit_dir.opposite
                        path_length += 1
                        break
                exits = maze.exits(current_loc)

            # If we've reached a deadend, don't log it
            current_tile = maze.at(current_loc)
            exits = maze.exits(current_loc)
            if len(exits) == 1 and current_tile.tile_type == BlockType.GROUND:
                continue

            # If we are here, then we've found a new node we can connect to, so add it to our exits
            FractalMazeGraph._make_path_and_find_new_exits(
                source_node=node,
                target_loc=current_loc,
                path_length=path_length,
                depth_increment=0,
                nodes=nodes,
                maze=maze
            )

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
        # "Priority queue" style Dijkstra implementation (faked using dict, so slower than should be)
        node_distances = {(0, self.entrance): 0}     # type: Dict[Tuple[int, MazeNode], int]
        nodes_to_explore = {(0, self.entrance)}      # type: Set[Tuple[int, MazeNode]]
        predecessor = {(0, self.entrance): None}     # type: Dict[Tuple[int, MazeNode], Optional[Tuple[int, MazeNode]]]

        while nodes_to_explore:
            current_depth, current_node = min(nodes_to_explore, key=lambda n: node_distances[n])
            if current_node.tile_type == BlockType.EXIT and current_depth == 0:
                break

            nodes_to_explore.remove((current_depth, current_node))

            for exit_path in current_node.exits:
                next_depth = current_depth + exit_path.depth_increment

                # If this path would leave the outermost ring, don't count it
                if next_depth < 0:
                    continue

                if (next_depth, exit_path.target) not in node_distances \
                        or node_distances[(current_depth, current_node)] + exit_path.length \
                           < node_distances[(next_depth, exit_path.target)]:
                    node_distances[(next_depth, exit_path.target)] \
                        = node_distances[(current_depth, current_node)] + exit_path.length
                    predecessor[(next_depth, exit_path.target)] = (current_depth, current_node)
                    nodes_to_explore.add((next_depth, exit_path.target))

        exit_node = None
        for depth, node in node_distances.keys():
            if node.tile_type == BlockType.EXIT:
                exit_node = node
                break

        path = [(0, exit_node)]
        while path[-1] != (0, self.entrance):
            path.append(predecessor[path[-1]])
        return node_distances[(0, exit_node)], reversed(path)

    def __str__(self):
        nodes_to_print = [self.entrance]
        nodes_printed = set()               # type: Set[Tuple[int,int]]
        s = ''
        while nodes_to_print:
            node = nodes_to_print.pop(-1)
            if node.loc not in nodes_printed:
                s += str(node) + '\n'
            nodes_printed.add(node.loc)
            for exit_path in node.exits:
                if exit_path.target.loc not in nodes_printed:
                    nodes_to_print.append(exit_path.target)
        return s.rstrip('\n')


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
        self.maze = FractalMaze.from_str(self.maze_str)

    def test_import_export(self):
        desired = textwrap.dedent("""\
         #######@#########
         #.#.............#
         #.#####.###.###.#
         #.#.....###...#.#
         #...###A#####.#.#
         #####       #.#.#
         a..##       ###.#
         ##.##       #.#.#
         ##..B       #.#.#
         #####       #.#.#
         ###.#####C###...#
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
        self.maze = FractalMaze.from_str(self.maze_str)
        self.maze.destroy_deadends()

    def test_destroy_deadends(self):
        desired = textwrap.dedent("""\
         #######@#########
         #######.........#
         #######.#######.#
         #######.#######.#
         #######A#######.#
         #####       ###.#
         a..##       ###.#
         ##.##       ###.#
         ##..B       ###.#
         #####       ###.#
         #########C#####.#
         b.#######...###.#
         #.#########.###.#
         c.#########.....#
         ###########$#####""")

        self.assertEqual(desired, str(self.maze))


class TestMazeGraph(unittest.TestCase):
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
        self.maze = FractalMaze.from_str(self.maze_str)
        self.maze.destroy_deadends()
        self.maze_graph = FractalMazeGraph.make(maze=self.maze)

    def test_mazegraph(self):
        desired = textwrap.dedent("""\
        (9, 2) --> [1: (9, 3)]
        (9, 3) --> [1: (9, 2); 3: (9, 6); 24: (13, 15)]
        (13, 15) --> [5: (11, 12); 1: (13, 16); 24: (9, 3)]
        (13, 16) --> [1: (13, 15)]
        (11, 12) --> [1: (2, 15); 5: (13, 15)]
        (2, 15) --> [1: (11, 12); 4: (2, 13)]
        (2, 13) --> [1: (6, 10); 4: (2, 15)]
        (6, 10) --> [1: (2, 13); 6: (2, 8)]
        (2, 8) --> [1: (9, 6); 6: (6, 10)]
        (9, 6) --> [1: (2, 8); 3: (9, 3)]""")

        self.assertEqual(desired, str(self.maze_graph))

    def test_shortest_path(self):
        desired = textwrap.dedent("""\
        (9, 2)[0], (9, 3)[0], (13, 15)[0], (13, 16)[0]""")

        length, shortest_path = self.maze_graph.shortest_path()
        length = int(length)
        path_str = ', '.join('({}, {})[{}]'.format(node.loc[0], node.loc[1], depth) for depth, node in shortest_path)
        self.assertEqual(26, length)
        self.assertEqual(desired, path_str)


class TestBigMazeGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.maze_str = textwrap.dedent("""\
                     Z L X W       C                 
                     Z P Q B       K                 
          ###########.#.#.#.#######.###############  
          #...#.......#.#.......#.#.......#.#.#...#  
          ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
          #.#...#.#.#...#.#.#...#...#...#.#.......#  
          #.###.#######.###.###.#.###.###.#.#######  
          #...#.......#.#...#...#.............#...#  
          #.#########.#######.#.#######.#######.###  
          #...#.#    F       R I       Z    #.#.#.#  
          #.###.#    D       E C       H    #.#.#.#  
          #.#...#                           #...#.#  
          #.###.#                           #.###.#  
          #.#....OA                       WB..#.#..ZH
          #.###.#                           #.#.#.#  
        CJ......#                           #.....#  
          #######                           #######  
          #.#....CK                         #......IC
          #.###.#                           #.###.#  
          #.....#                           #...#.#  
          ###.###                           #.#.#.#  
        XF....#.#                         RF..#.#.#  
          #####.#                           #######  
          #......CJ                       NM..#...#  
          ###.#.#                           #.###.#  
        RE....#.#                           #......RF
          ###.###        X   X       L      #.#.#.#  
          #.....#        F   Q       P      #.#.#.#  
          ###.###########.###.#######.#########.###  
          #.....#...#.....#.......#...#.....#.#...#  
          #####.#.###.#######.#######.###.###.#.#.#  
          #.......#.......#.#.#.#.#...#...#...#.#.#  
          #####.###.#####.#.#.#.#.###.###.#.###.###  
          #.......#.....#.#...#...............#...#  
          #############.#.#.###.###################  
                       A O F   N                     
                       A A D   M                     """)
        self.maze = FractalMaze.from_str(self.maze_str)
        self.maze.destroy_deadends()
        self.maze_graph = FractalMazeGraph.make(maze=self.maze)

    def test_shortest_path(self):
        length, shortest_path = self.maze_graph.shortest_path()
        length = int(length)
        path_str = ', '.join('({}, {})[{}]'.format(node.loc[0], node.loc[1], depth) for depth, node in shortest_path)
        self.assertEqual(396, length, msg=path_str)


if __name__ == "__main__":
    unittest.main()
