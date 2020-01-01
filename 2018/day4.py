from getinput import get_input
import itertools
import textwrap
import datetime
from collections import defaultdict


class Guard(object):
    def __init__(self):
        self.id = None
        self.falls_asleep = []
        self.wakes_up = []

    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.falls_asleep, self.wakes_up)

    def __repr__(self):
        return '{}: {}, {}'.format(self.id, self.falls_asleep, self.wakes_up)

    @property
    def mins_asleep(self):
        if len(self.falls_asleep) != len(self.wakes_up):
            raise RuntimeError('Bad guard')
        return sum(wake - sleep for sleep, wake in zip(self.falls_asleep, self.wakes_up))

    def asleep_at(self, minute):
        wakeups = [t for t in self.wakes_up if t <= minute]
        sleeps = [t for t in self.falls_asleep if t <= minute]
        if not sleeps:
            return False
        if not wakeups:
            return True
        return max(wakeups) < max(sleeps)


def parse_input(s):
    guards = defaultdict(lambda: Guard())

    for line in s.splitlines(keepends=False):
        timestamp = datetime.datetime.strptime(line[0:18], '[%Y-%m-%d %H:%M]')
        date = timestamp.date()
        if timestamp.hour == 23:
            date = date + datetime.timedelta(days=1)
        day_number = (date - datetime.date(year=date.year, month=1, day=1)).days

        words = line[19:].split()

        if words[0] == 'Guard':
            guards[day_number].id = int(words[1].lstrip('#'))
        elif words[0] == 'wakes':
            guards[day_number].wakes_up.append(timestamp.minute)
        elif words[0] == 'falls':
            guards[day_number].falls_asleep.append(timestamp.minute)
    return guards


def part_1(input_str):
    # input_str = test_input()
    guards = parse_input(input_str)
    guard_sleep_tallies = defaultdict(lambda: 0)
    for day, guard in guards.items():
        guard_sleep_tallies[guard.id] += guard.mins_asleep

    sleepiest_guard = max(guard_sleep_tallies.keys(), key=lambda g: guard_sleep_tallies[g])
    instances = list(g for g in guards.values() if g.id == sleepiest_guard)

    num_times_asleep = dict()
    for minute in range(60):
        num_times_asleep[minute] = sum(g.asleep_at(minute) for g in instances)
    return sleepiest_guard*max(num_times_asleep.keys(), key=lambda m: num_times_asleep[m])


def part_2(input_str):
    # input_str = test_input()
    guards = parse_input(input_str)
    guard_sleep_tallies = defaultdict(lambda: 0)
    for day, guard in guards.items():
        for minute in range(60):
            guard_sleep_tallies[(guard.id, minute)] += 1 if guard.asleep_at(minute) else 0

    sleepiest_guard, sleepiest_minute = max(guard_sleep_tallies.keys(), key=lambda x: guard_sleep_tallies[x])
    return sleepiest_guard*sleepiest_minute


def test_input():
    return textwrap.dedent("""\
    [1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up""")


def main():
    input_str = get_input(4)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
