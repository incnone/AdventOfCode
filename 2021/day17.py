import textwrap


def get_test_input() -> str:
    return textwrap.dedent("""\
    target area: x=20..30, y=-10..-5""")


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
        words = line.split()
        xcoords = tuple(int(x) for x in words[2][2:-1].split('..'))
        ycoords = tuple(int(x) for x in words[3][2:].split('..'))
        data.append((xcoords, ycoords))
    return data


class Rect(object):
    def __init__(self, xbounds, ybounds):
        self.left, self.right = xbounds
        self.bottom, self.top = ybounds

    def contains(self, pt):
        return self.left <= pt[0] <= self.right and self.bottom <= pt[1] <= self.top


class Probe(object):
    def __init__(self, init_vel, target: Rect):
        self._pos = (0, 0)
        self._prevpos = (0, 0)
        self._init_vel = init_vel
        self._vel = init_vel
        self.hits = False
        self.too_far = False
        self.max_y_pos = 0

        while True:
            if self._pos[0] > target.right:
                self.too_far = not target.bottom <= self._prevpos[1] <= target.top
                break
            elif self._pos[0] < target.left and self._vel[0] == 0:
                break
            elif self._pos[1] < target.bottom:
                break
            elif target.contains(self._pos):
                self.hits = True
            self._step()

    def _step(self):
        self._prevpos = self._pos
        self._pos = (self._pos[0] + self._vel[0], self._pos[1] + self._vel[1])
        self._vel = (max(self._vel[0] - 1, 0), self._vel[1] - 1)
        self.max_y_pos = max(self._pos[1], self.max_y_pos)


def part_1(data):
    target = Rect(*data[0])
    any_successes = False
    max_y_pos = 0
    num_successes = 0
    for yvel in range(-105, 105):
        xvel = 0
        any_xvel_worked = False
        too_far = False
        while not too_far:
            xvel += 1
            probe = Probe((xvel, yvel), target)
            any_xvel_worked |= probe.hits
            any_successes |= probe.hits
            if probe.hits:
                max_y_pos = probe.max_y_pos
                num_successes += 1
            too_far = probe.too_far
    print(f'Part 1: {max_y_pos}')
    print(f'Part 2: {num_successes}')


def part_2(data):
    pass


def main():
    data = read_input(day_number=17, test=False)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
