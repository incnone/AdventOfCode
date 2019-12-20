from torusmaze import TorusMaze, TorusMazeGraph
from fractalmaze import FractalMaze, FractalMazeGraph


def part_1(puzzle_input):
    maze = TorusMaze.from_str(puzzle_input)
    maze.destroy_deadends()
    maze_graph = TorusMazeGraph.make(maze)
    length, path = maze_graph.shortest_path()
    return length


def part_2(puzzle_input):
    maze = FractalMaze.from_str(puzzle_input)
    maze.destroy_deadends()
    maze_graph = FractalMazeGraph.make(maze)
    length, path = maze_graph.shortest_path()
    return length, path


if __name__ == '__main__':
    with open('input/dec20.txt', 'r') as file:
        maze_str = file.read()

    print('Part 1: ', part_1(puzzle_input=maze_str))
    length, shortest_path = part_2(puzzle_input=maze_str)
    print('Part 2: ', length)
