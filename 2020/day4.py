import textwrap


class Passport(object):
    all_fields = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        'cid'
    ]

    def __init__(self, s: str):
        self.data = dict()
        for field in s.split():
            k, v = field.split(':')
            self.data[k] = v

    def __str__(self):
        return ' '.join(['{}:{}'.format(k, v) for k,v in self.data.items()])

    @property
    def has_all_required_fields(self):
        for field in Passport.all_fields:
            if field != 'cid' and field not in self.data:
                return False
        return True

    @property
    def is_vaild(self) -> bool:
        return self._valid_byr and self._valid_iyr and self._valid_eyr and self._valid_hgt and self._valid_hcl \
               and self._valid_ecl and self._valid_pid

    @property
    def valid_data_str(self) -> str:
        return textwrap.dedent("""\
        Byr: {byr}; Iyr: {iyr}; Eyr: {eyr}; Hgt: {hgt}; Hcl: {hcl}; Ecl: {ecl}; Pid: {pid}""".format(
            byr=str(self._valid_byr),
            eyr=str(self._valid_eyr),
            iyr=str(self._valid_iyr),
            hgt=str(self._valid_hgt),
            hcl=str(self._valid_hcl),
            ecl=str(self._valid_ecl),
            pid=str(self._valid_pid),
        ))

    @property
    def _valid_byr(self):
        try:
            byr = int(self.data['byr'])
            if byr < 1920 or byr > 2002:
                return False
            return True
        except (ValueError, KeyError):
            return False

    @property
    def _valid_iyr(self):
        try:
            iyr = int(self.data['iyr'])
            if iyr < 2010 or iyr > 2020:
                return False
            return True
        except (ValueError, KeyError):
            return False

    @property
    def _valid_eyr(self):
        try:
            eyr = int(self.data['eyr'])
            if eyr < 2020 or eyr > 2030:
                return False
            return True
        except (ValueError, KeyError):
            return False

    @property
    def _valid_hgt(self):
        try:
            hgt = int(self.data['hgt'][:-2])
            hgt_unit = self.data['hgt'][-2:]
            if hgt_unit != 'cm' and hgt_unit != 'in':
                return False
            if hgt_unit == 'cm' and (hgt < 150 or hgt > 193):
                return False
            if hgt_unit == 'in' and (hgt < 59 or hgt > 76):
                return False
            return True
        except (ValueError, KeyError):
            return False

    @property
    def _valid_hcl(self):
        try:
            hcl = self.data['hcl']
            if len(hcl) != 7 or not hcl[0] == '#':
                return False
            int(hcl[1:], 16)
            return True
        except (ValueError, KeyError):
            return False

    @property
    def _valid_ecl(self):
        try:
            ecl = self.data['ecl']
            if ecl not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
                return False
            return True
        except KeyError:
            return False

    @property
    def _valid_pid(self):
        try:
            pid = self.data['pid']
            if len(pid) != 9 or not pid.isdigit():
                return False
            return True
        except KeyError:
            return False


def get_test_input() -> str:
    return textwrap.dedent("""\
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm
    
    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929
    
    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm
    
    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in
    """)


def read_input(day_number, test=False):
    if test:
        return parse_input(get_test_input())
    else:
        filename = 'input/dec{}.txt'.format(day_number)
        with open(filename, 'r') as file:
            return parse_input(file.read())


def parse_input(s: str):
    data = []
    for line in s.split('\n\n'):
        data.append(Passport(line))
    return data


def part_1(data):
    count = 0
    for passport in data:
        if passport.has_all_required_fields:
            count += 1
    print("Part 1:", count)


def part_2(data):
    count = 0
    for passport in data:
        if passport.is_vaild:
            count += 1
    print("Part 2:", count)


def p2_test():
    invalids = textwrap.dedent("""\
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
    
    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946
    
    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
    
    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007""")

    valids = textwrap.dedent("""\
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f
    
    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
    
    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022
    
    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")

    vaild_pass = parse_input(valids)
    invalid_pass = parse_input(invalids)

    for passport in vaild_pass:
        if not passport.is_vaild:
            print("Valid passport incorrectly marked invalid:\n", passport)
            print(passport.valid_data_str)

    for passport in invalid_pass:
        if passport.is_vaild:
            print("Invalid passport incorrectly marked valid:\n", passport)
            print(passport.valid_data_str)


def main():
    data = read_input(day_number=4, test=False)
    part_1(data)
    p2_test()
    part_2(data)


if __name__ == "__main__":
    main()
