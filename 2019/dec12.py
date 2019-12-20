def sign(x):
    return x and (1, -1)[x < 0]


class Moon(object):
    def __init__(self, loc):
        self.loc = list(loc)
        self.velocity = [0, 0, 0]

    def apply_gravity(self, other):
        for idx in range(3):
            self.velocity[idx] += sign(other.loc[idx] - self.loc[idx])

    def apply_velocity(self):
        for idx in range(3):
            self.loc[idx] += self.velocity[idx]

    @property
    def potential_energy(self):
        return abs(self.loc[0]) + abs(self.loc[1]) + abs(self.loc[2])

    @property
    def kinetic_energy(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


class MoonSystem(object):
    def __init__(self, moons):
        self.moons = moons

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for moon in self.moons:
            for other in self.moons:
                if moon != other:
                    moon.apply_gravity(other)

    def apply_velocity(self):
        for moon in self.moons:
            moon.apply_velocity()

    @property
    def total_energy(self):
        return sum([m.total_energy for m in self.moons])

    def coords_at_idx(self, idx):
        return [m.loc[idx] for m in self.moons]

    def velos_at_idx(self, idx):
        return [m.velocity[idx] for m in self.moons]


if __name__ == "__main__":
    starting_positions = [
        (-4, 3, 15),
        (-11, -10, 13),
        (2, 2, 18),
        (7, -1, 0)
    ]

    periods = []
    for idx in range(3):
        starts = [t[idx] for t in starting_positions]
        moons = []
        for t in starting_positions:
            new_moon = Moon(t)
            moons.append(new_moon)

        system = MoonSystem(moons)

        step_count = 1
        system.step()
        while system.coords_at_idx(idx) != starts or system.velos_at_idx(idx) != [0, 0, 0, 0]:
            system.step()
            step_count += 1
        periods.append(step_count)

    print(periods)
