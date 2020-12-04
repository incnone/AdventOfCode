import re


class Password(object):
    def __init__(self, password: str, minval: int, maxval: int, needed: str):
        self.password = password
        self.minval = minval
        self.maxval = maxval
        self.needed = needed

    def valid_1(self):
        return self.minval <= self.password.count(self.needed) <= self.maxval

    def valid_2(self):
        return (self.password[self.minval-1] == self.needed) ^ (self.password[self.maxval-1] == self.needed)


def read_input(day_num: int):
    data = []
    pattern = re.compile(r'(?P<minval>\d*)-(?P<maxval>\d*) (?P<needed>\w): (?P<pswd>\w*)')
    filename = 'input/dec{}.txt'.format(day_num)
    with open(filename, 'r') as file:
        for line in file:
            vals = pattern.match(line)
            data.append(Password(
                password=vals['pswd'],
                minval=int(vals['minval']),
                maxval=int(vals['maxval']),
                needed=vals['needed']
            ))
    return data


def part_1(data):
    count = 0
    for e in data:
        count += 1 if e.valid_1() else 0
    print("Part 1: {} valid passwords.".format(count))


def part_2(data):
    count = 0
    for e in data:
        count += 1 if e.valid_2() else 0
    print("Part 1: {} valid passwords.".format(count))


def main():
    data = read_input(2)
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
