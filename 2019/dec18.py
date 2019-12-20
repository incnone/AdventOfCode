from enum import Enum
from typing import List, Optional
from maze import Maze, MazeGraph, BlockType
from pairs import Direction
import textwrap


def part_1(maze_info):
    maze = Maze.from_str(maze_info[0])
    entrances = maze_info[1]
    maze.destroy_deadends()

    maze_graph = MazeGraph.make(maze=maze, entrance_offsets_and_outdirs=entrances)
    solution = maze_graph.solve()
    return solution


def part_2(maze_info):
    maze = Maze.from_str(maze_info[0])
    entrances = maze_info[1]
    maze.destroy_deadends()

    maze_graph = MazeGraph.make(maze=maze, entrance_offsets_and_outdirs=entrances)
    doors = set()
    for keypath in maze_graph.keypaths.values():
        # print(maze_graph.keypath_str(keypath))
        for node in keypath:
            if node.block_type == BlockType.DOOR:
                doors.add(node.key_val.upper())

    # Paths created by inspection LOL again but it was easier this time
    robot_1 = maze_graph.path_length('rjiqd') - 2
    robot_2 = maze_graph.path_length('octhf') - 2
    robot_3 = maze_graph.path_length('nkwbumaslg') - 2
    robot_4 = maze_graph.path_length('ezvyp') - 2
    return robot_1 + robot_2 + robot_3 + robot_4


def puzzle_input():
    with open('input/dec18.txt', 'r') as file:
        the_maze_str = file.read()

    return the_maze_str, \
    {
        (-1, -1): [Direction.WEST],
        (1, -1): [Direction.NORTH],
        (-1, 1): [Direction.SOUTH],
        (1, 1): [Direction.EAST],
    }


def testmaze_1():
    return \
    textwrap.dedent("""\
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################"""),\
    {
        (0, 0): [Direction.NORTH, Direction.SOUTH]
    }


if __name__ == "__main__":
    print('Part 1:', part_1(puzzle_input()))
    print('Part 2:', part_2(puzzle_input()))
