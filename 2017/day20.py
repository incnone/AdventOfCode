from getinput import get_input
import itertools
from collections import Counter


class Particle(object):
    def __init__(self, n, p, v, a):
        self.n = n
        self.p = p
        self.v = v
        self.a = a

    def __str__(self):
        return 'P(p={}, v={}, a={})'.format(self.p, self.v, self.a)

    def __repr__(self):
        return 'P{}(p={}, v={}, a={})'.format(self.n, self.p, self.v, self.a)

    def tick(self):
        self.v = (self.v[0] + self.a[0], self.v[1] + self.a[1], self.v[2] + self.a[2])
        self.p = (self.p[0] + self.v[0], self.p[1] + self.v[1], self.p[2] + self.v[2])

    def dist(self):
        return sum(abs(x) for x in self.p)


def parse_word(s):
    return tuple(int(x) for x in s.strip('pva<,>=').split(','))


def parse_line(idx, s):
    return Particle(idx, *[parse_word(w) for w in s.split()])


def parse_input(s):
    return list(parse_line(idx, line) for idx, line in enumerate(s.splitlines(keepends=False)))


def part_1(input_str):
    particles = parse_input(input_str)
    for _ in range(1000):
        for p in particles:
            p.tick()

    return min(particles, key=lambda x: x.dist()).n


def part_2(input_str):
    particles = parse_input(input_str)
    for _ in range(1000):
        to_destroy = []
        particle_locs = Counter(particle.p for particle in particles)

        for idx, p in enumerate(particles):
            if particle_locs[p.p] > 1:
                to_destroy.append(idx)
            else:
                p.tick()

        for idx in reversed(to_destroy):
            particles.pop(idx)

    return len(particles)


def main():
    input_str = get_input(20)
    print('Part 1:', part_1(input_str))
    print('Part 2:', part_2(input_str))


if __name__ == "__main__":
    main()
