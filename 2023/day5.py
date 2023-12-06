import textwrap
from typing import Tuple, List
import bisect
import itertools


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def get_test_input() -> str:
    return textwrap.dedent("""\
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48
    
    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15
    
    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4
    
    water-to-light map:
    88 18 7
    18 25 70
    
    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13
    
    temperature-to-humidity map:
    0 69 1
    1 0 69
    
    humidity-to-location map:
    60 56 37
    56 93 4""")


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/day{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    return MapData(s.splitlines(keepends=False))


class MapData(object):
    def __init__(self, lines: List[str]):
        self.debug = False
        self.seeds = [int(x) for x in lines[0].split()[1:]]

        self.seed_soil = PiecewiseMap('soil')
        self.soil_fert = PiecewiseMap('fert')
        self.fert_water = PiecewiseMap('water')
        self.water_light = PiecewiseMap('light')
        self.light_temp = PiecewiseMap('temp')
        self.temp_hum = PiecewiseMap('hum')
        self.hum_loc = PiecewiseMap('loc')
        curmap = None

        whichmap = {
            'se': self.seed_soil,
            'so': self.soil_fert,
            'fe': self.fert_water,
            'wa': self.water_light,
            'li': self.light_temp,
            'te': self.temp_hum,
            'hu': self.hum_loc
        }

        for line in lines:
            if len(line) < 2:
                continue

            firstchars = line[:2]
            if firstchars in whichmap:
                curmap = whichmap[firstchars]
                continue

            curmap.add_vals([int(x) for x in line.split()])

        for m in whichmap.values():
            m.sort_vals_and_lock()

    def get_image_of_interval_list(self, ilist):
        soil = self.seed_soil.get_image_of_interval_list(ilist)
        fert = self.soil_fert.get_image_of_interval_list(soil)
        wat = self.fert_water.get_image_of_interval_list(fert)
        light = self.water_light.get_image_of_interval_list(wat)
        temp = self.light_temp.get_image_of_interval_list(light)
        hum = self.temp_hum.get_image_of_interval_list(temp)
        loc = self.hum_loc.get_image_of_interval_list(hum)
        return loc

    def get_image_of_interval_list_debug(self, ilist):
        print(f'IList: {ilist}')
        soil = self.seed_soil.get_image_of_interval_list(ilist)
        print(f'Soul: {soil}')
        fert = self.soil_fert.get_image_of_interval_list(soil)
        print(f'Fert: {fert}')
        wat = self.fert_water.get_image_of_interval_list(fert)
        print(f'Water: {wat}')
        light = self.water_light.get_image_of_interval_list(wat)
        print(f'Light: {light}')
        temp = self.light_temp.get_image_of_interval_list(light)
        print(f'Temp: {temp}')
        hum = self.temp_hum.get_image_of_interval_list(temp)
        print(f'Hum: {hum}')
        loc = self.hum_loc.get_image_of_interval_list(hum)
        print(f'Loc: {loc}')
        return loc

    def __call__(self, x: int):
        if self.debug:
            return self._call_debug(x)
        else:
            return self._call_nodebug(x)

    def _call_nodebug(self, x: int):
        x = self.seed_soil(x)
        x = self.soil_fert(x)
        x = self.fert_water(x)
        x = self.water_light(x)
        x = self.light_temp(x)
        x = self.temp_hum(x)
        x = self.hum_loc(x)
        return x

    def _call_debug(self, seed: int):
        soil = self.seed_soil(seed)
        fert = self.soil_fert(soil)
        wat = self.fert_water(fert)
        light = self.water_light(wat)
        temp = self.light_temp(light)
        hum = self.temp_hum(temp)
        loc = self.hum_loc(hum)
        print(f'Seed {seed}, soil {soil}, fert {fert}, water {wat}, light {light}, temp {temp}, hum {hum}, loc {loc}')
        return loc


class PiecewiseMap(object):
    def __init__(self, name=None):
        self.name = name
        self._all = []
        self._sources = []
        self._dests = []
        self._ranges = []
        self._islocked = False

    def add_vals(self, vals: List[int]):
        assert len(vals) == 3 and not self._islocked
        self._all.append(vals)

    def sort_vals_and_lock(self):
        self._islocked = True
        self._all.sort(key=lambda x: x[1])
        for d, s, r in self._all:
            self._sources.append(s)
            self._dests.append(d)
            self._ranges.append(r)

    def get_image_of_interval(self, left: int, length: int) -> List[Tuple[int, int]]:
        image_intervals = []
        used_left_vals = []
        used_right_vals = [left]
        for d, s, r in self._all:
            this_left = max(left, s)
            this_right = min(left + length, s + r)
            if this_left < this_right:
                image_intervals.append((d + (this_left - s), this_right - this_left))
                used_left_vals.append(this_left)
                used_right_vals.append(this_right)
        used_left_vals.append(left + length)
        for l, r in zip(used_right_vals, used_left_vals):  # intentional swap of left-right
            if r - l > 0:
                image_intervals.append((l, r - l))
        return image_intervals

    def get_image_of_interval_list(self, interval_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        image_intervals = []
        for a, b in interval_list:
            image_intervals += self.get_image_of_interval(a, b)
        return image_intervals

    def __call__(self, x: int):
        lower_src_idx = bisect.bisect_right(self._sources, x) - 1
        if lower_src_idx < 0:
            return x
        the_source = self._sources[lower_src_idx]
        the_range = self._ranges[lower_src_idx]
        if x >= the_source + the_range:
            return x
        return self._dests[lower_src_idx] + (x - the_source)

    def __repr__(self):
        return self.name


def part_1(data):
    locations = dict()
    for seed in data.seeds:
        locations[seed] = data(seed)

    print(f'Part 1: {min(locations.values())}')


def part_2(data):
    seed_intervals = [(a, b) for a, b in batched(data.seeds, 2)]
    loc_intervals = data.get_image_of_interval_list(seed_intervals)
    print(f'Part 2: {min(loc_intervals, key=lambda x: x[0])[0]}')


def main():
    data = read_input(day_number=5, test=False)
    # part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
