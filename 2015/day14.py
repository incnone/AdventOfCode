from getinput import get_input
import itertools
import textwrap


class Reindeer(object):
    def __init__(self, speed, sustain_time, rest_time):
        self.loc = 0
        self.speed = speed
        self.sustain_time = sustain_time
        self.rest_time = rest_time

        self.resting = False
        self.cycles_until_change = self.sustain_time

    def run(self):
        if not self.resting:
            self.loc += self.speed
        self.cycles_until_change -= 1
        if self.cycles_until_change == 0:
            if self.resting:
                self.resting = False
                self.cycles_until_change = self.sustain_time
            else:
                self.resting = True
                self.cycles_until_change = self.rest_time


def parse_flight_string(s):
    words = s.split()
    return words[0], int(words[3]), int(words[6]), int(words[13])


def parse_input(big_str):
    flight_info = dict()
    for line in big_str.splitlines(keepends=False):
        flyer, speed, sustain_time, rest_time = parse_flight_string(line)
        flight_info[flyer] = (speed, sustain_time, rest_time)
    return flight_info


def travel(num_seconds, speed, sustain_time, rest_time):
    cycle_time = sustain_time + rest_time
    travel_time = (num_seconds // cycle_time)*sustain_time + min(num_seconds % cycle_time, sustain_time)
    return travel_time*speed


def part_1(flight_dict):
    travel_lengths = dict()
    num_seconds = 2503
    for flyer, travel_info in flight_dict.items():
        travel_lengths[flyer] = travel(num_seconds, *travel_info)

    return max(travel_lengths.values())


def part_2(flight_dict):
    reindeer_dict = dict()
    reindeer_points = dict()
    num_seconds = 2503
    for flyer, travel_info in flight_dict.items():
        reindeer_dict[flyer] = Reindeer(*travel_info)
        reindeer_points[flyer] = 0

    for _ in range(num_seconds):
        max_so_far = -1
        furthest_reindeer = []
        for name, reindeer in reindeer_dict.items():
            reindeer.run()
            if reindeer.loc > max_so_far:
                max_so_far = reindeer.loc
                furthest_reindeer = [name]
            elif reindeer.loc == max_so_far:
                furthest_reindeer.append(name)
        for name in furthest_reindeer:
            reindeer_points[name] += 1

    return max(reindeer_points.values())


def test_input():
    return textwrap.dedent("""\
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.""")


if __name__ == "__main__":
    the_flight_dict = parse_input(get_input(day=14))
    # the_flight_dict = parse_input(test_input())

    print('Part 1:', part_1(the_flight_dict))
    print('Part 2:', part_2(the_flight_dict))
