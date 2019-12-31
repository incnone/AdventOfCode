from getinput import get_input
from maze import Maze, BlockType
from travelling import shortest_route, shortest_circuit
import textwrap


def part_1(keydists):
    return shortest_route(distances=keydists, start='0')[1]


def part_2(keydists):
    return shortest_circuit(distances=keydists, start='0')[1]


def test_input():
    return textwrap.dedent("""\
    ###########
    #0.1.....2#
    #.#######.#
    #4.......3#
    ###########""")


if __name__ == "__main__":
    the_big_str = get_input(24)
    the_maze = Maze.from_str(the_big_str)
    the_maze.destroy_deadends()
    the_keydists = the_maze.get_keydists()

    print('Part 1:', part_1(the_keydists))
    print('Part 2:', part_2(the_keydists))
