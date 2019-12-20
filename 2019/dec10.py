import copy
from fractions import Fraction


def sieve_asteroids(loc, asteroid_field):
    # Sieve down
    _sieve_asteroids_vert_hlpr(loc, asteroid_field, 1)
    # Sieve up
    _sieve_asteroids_vert_hlpr(loc, asteroid_field, -1)
    # Sieve same row left
    _sieve_asteroids_row_hlpr(loc, asteroid_field, -1)
    # Sieve same row right
    _sieve_asteroids_row_hlpr(loc, asteroid_field, 1)


def _sieve_asteroids_row_hlpr(loc, asteroid_field, step):
    found = False
    endpoint = -1 if step == -1 else len(asteroid_field[0])
    for x in range(loc[0] + step, endpoint, step):
        if asteroid_field[loc[1]][x]:
            if found:
                asteroid_field[loc[1]][x] = 0
            else:
                found = True


def _sieve_asteroids_vert_hlpr(loc, asteroid_field, vert_step):
    """vert_step must be -1, 0, or 1"""
    field_width = len(asteroid_field[0])
    field_height = len(asteroid_field)

    if vert_step == 0:
        # TODO: sieve row
        return

    endpoint = field_height if vert_step == 1 else -1
    for y1 in range(loc[1] + vert_step, endpoint, vert_step):
        for y2 in range(y1 + vert_step, endpoint, vert_step):
            ratio = Fraction(numerator=(y1 - loc[1]), denominator=(y2 - loc[1]))
            r1_step = ratio.numerator
            r2_step = ratio.denominator
            n_left = (loc[0] // r2_step)
            n_right = (field_width - loc[0]) // r2_step + 1
            for x1, x2 in zip(
                    range(loc[0] - n_left*r1_step, loc[0] + n_right*r1_step, r1_step),
                    range(loc[0] - n_left*r2_step, loc[0] + n_right*r2_step, r2_step)
            ):
                if asteroid_field[y1][x1]:
                    try:
                        asteroid_field[y2][x2] = 0
                    except IndexError:
                        pass
                        # print('IndexError: Base ({}, {}), projecting ({}, {}) onto ({}, {}); ratio {}'.format(
                        #     loc[0], loc[1], x1, y1, x2, y2, ratio)
                        # )


def num_visible_asteroids(loc, asteroid_field):
    visible_asteroids = copy.deepcopy(asteroid_field)
    sieve_asteroids(loc, visible_asteroids)
    return sum([a for row in visible_asteroids for a in row]) - 1


def find_number_detected_str(asteroid_field):
    number_detected = [['.']*len(asteroid_field[0]) for _ in range(len(asteroid_field))]
    for row in range(len(asteroid_field)):
        for col in range(len(asteroid_field[0])):
            if asteroid_field[row][col] == 1:
                number_detected[row][col] = str(num_visible_asteroids((col, row), asteroid_field))

    return number_detected


def find_number_detected(asteroid_field):
    number_detected = [[0]*len(asteroid_field[0]) for _ in range(len(asteroid_field))]
    for row in range(len(asteroid_field)):
        for col in range(len(asteroid_field[0])):
            if asteroid_field[row][col] == 1:
                number_detected[row][col] = num_visible_asteroids((col, row), asteroid_field)

    return number_detected


def find_best_station_locs(asteroid_field):
    best_number_so_far = 0
    best_stations_so_far = []
    for row in range(len(asteroid_field)):
        for col in range(len(asteroid_field[0])):
            if asteroid_field[row][col] == 1:
                num = num_visible_asteroids((col, row), asteroid_field)
                if num > best_number_so_far:
                    best_number_so_far = num
                    best_stations_so_far = [(col, row)]
                elif num == best_number_so_far:
                    best_stations_so_far.append((col, row))

    return best_stations_so_far, best_number_so_far


def get_asteroid_field_str(asteroid_field):
    return '\n'.join([''.join(['#' if c else '.' for c in r]) for r in asteroid_field])


class HomogCoords(object):
    """Store (x, y) but only to rational lowest terms, order by -y/x, Q1<Q4<Q3<Q2"""
    def __init__(self, x, y):
        if x == 0:
            if y == 0:
                raise RuntimeError('Can\'t make HomogCoords with both x and y zero')
            self.x = 0
            self.y = 1 if y > 0 else -1
        else:
            frac = Fraction(numerator=y, denominator=x)
            self.x = abs(frac.denominator) if x > 0 else -abs(frac.denominator)
            self.y = abs(frac.numerator) if y > 0 else -abs(frac.numerator)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not(self.__eq__(other))

    def __lt__(self, other):
        if self.x == 0:
            if self.y == -1:
                return self != other
            else:  # self.y == 1
                return other.x < 0
        elif other.x == 0:
            if other.y == -1:
                return False
            else:  # other.y == 1
                return self.x > 0
        elif self.x < 0 < other.x:
            return False
        elif other.x < 0 < self.x:
            return True
        else:
            return self.y*other.x < self.x*other.y

    def __gt__(self, other):
        return self != other and not self < other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


def get_vaporization_order(laser_loc, asteroid_field):
    class Asteroid(object):
        def __init__(self, loc):
            self.loc = loc
            self.disp = HomogCoords(loc[0] - laser_loc[0], loc[1] - laser_loc[1])
            self.sup_dist = max(abs(loc[0] - laser_loc[0]), abs(loc[1] - laser_loc[1]))
            self.vapo_idx = 0

        def __repr__(self):
            return str(self.loc)

    asteroid_list = []

    for y in range(len(asteroid_field)):
        for x in range(len(asteroid_field[0])):
            if asteroid_field[y][x] == 1 and (x, y) != laser_loc:
                asteroid_list.append(Asteroid((x, y)))

    asteroid_list = sorted(asteroid_list, key=lambda a: (a.disp, a.sup_dist))
    last_vapo_idx = 0
    last_disp = asteroid_list[0].disp
    for asteroid in asteroid_list[1:]:
        if asteroid.disp == last_disp:
            last_vapo_idx += 1
            asteroid.vapo_idx = last_vapo_idx
        else:
            last_disp = asteroid.disp
            last_vapo_idx = 0

    return sorted(asteroid_list, key=lambda a: (a.vapo_idx, a.disp, a.sup_dist))


def test_1():
    test = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.........###..
..#.#.....#....##"""
    test_station = (8, 3)
    test_asteroids = []
    for line in test.splitlines():
        test_asteroids.append(list([(1 if c == '#' else 0) for c in line.rstrip('\n')]))

    vapo_order = get_vaporization_order(test_station, test_asteroids)

    for a in vapo_order:
        print(a.loc, str(a.disp), a.vapo_idx)


def test_2():
    test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    test_station = (11, 13)
    test_asteroids = []
    for line in test.splitlines():
        test_asteroids.append(list([(1 if c == '#' else 0) for c in line.rstrip('\n')]))

    vapo_order = get_vaporization_order(test_station, test_asteroids)
    print(vapo_order[0:3], vapo_order[9], vapo_order[19], vapo_order[49], vapo_order[99], vapo_order[198:201])


def actual():
    with open("input/dec10.txt", 'r') as file:
        asteroids = []
        for line in file:
            asteroids.append(list([(1 if c == '#' else 0) for c in line.rstrip('\n')]))

    # print(find_best_station_locs(asteroid_field=asteroids))
    best_station = (20, 19)
    vapo_order = get_vaporization_order(best_station, asteroids)
    print(vapo_order[199])


if __name__ == "__main__":
    actual()


