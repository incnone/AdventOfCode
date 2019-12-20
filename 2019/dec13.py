from enum import Enum
from intcode import IntcodeProgram


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZ_PADDLE = 3
    BALL = 4

    def get_char(self):
        if self == TileType.EMPTY:
            return ' '
        elif self == TileType.WALL:
            return '#'
        elif self == TileType.BLOCK:
            return 'X'
        elif self == TileType.HORIZ_PADDLE:
            return '-'
        elif self == TileType.BALL:
            return 'o'


class BlockGame(object):
    def __init__(self):
        self.tiles = dict()
        self.score = 0
        self.paddle_x = None
        self.ball_x = None
        self.output_cache = []

    def interpret(self, x):
        if x[0] == -1 and x[1] == 0:
            self.score = x[2]
            return

        tile_type = TileType(x[2])
        self.tiles[(x[0], x[1])] = tile_type
        if tile_type == TileType.HORIZ_PADDLE:
            self.paddle_x = x[0]
        elif tile_type == TileType.BALL:
            self.ball_x = x[0]

    def get_input(self):
        if self.paddle_x is None or self.ball_x is None:
            return 0
        elif self.paddle_x > self.ball_x:
            return -1
        elif self.paddle_x < self.ball_x:
            return 1
        else:
            return 0

    def read_output(self, value):
        self.output_cache.append(value)
        if len(self.output_cache) == 3:
            self.interpret(self.output_cache)
            self.output_cache = []

    def get_picture(self):
        min_x = min([x[0] for x in self.tiles.keys()])
        max_x = max([x[0] for x in self.tiles.keys()])
        min_y = min([x[1] for x in self.tiles.keys()])
        max_y = max([x[1] for x in self.tiles.keys()])

        ret = ''
        for y in range(min_y, max_y+1, 1):
            for x in range(min_x, max_x + 1, 1):
                if (x, y) in self.tiles:
                    ret += self.tiles[(x, y)].get_char()
                else:
                    ret += ' '
            ret += '\n'

        ret += '\n'
        ret += "Score: {}\n".format(self.score)
        return ret


if __name__ == "__main__":
    with open('input/dec13.txt', 'r') as file:
        program_code = file.readline()

    block_game = BlockGame()
    program = IntcodeProgram(program_code, inputter=block_game, outputter=block_game)
    program.code[0] = 2
    program.execute()

    print(block_game.score)
