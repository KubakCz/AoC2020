from typing import List, Optional


class Passport:
    def __init__(self):
        self.byr: Optional[str] = None
        self.iyr: Optional[str] = None
        self.eyr: Optional[str] = None
        self.hgt: Optional[str] = None
        self.hcl: Optional[str] = None
        self.ecl: Optional[str] = None
        self.pid: Optional[str] = None
        self.cid: Optional[str] = None

    def contains_all_fields(self) -> bool:
        return self.byr is not None and \
            self.iyr is not None and \
            self.eyr is not None and \
            self.hgt is not None and \
            self.hcl is not None and \
            self.ecl is not None and \
            self.pid is not None

    def is_valid_byr(self) -> bool:
        return self.byr is not None and \
            len(self.byr) == 4 and \
            self.byr.isdigit() and \
            1920 <= int(self.byr) <= 2002

    def is_valid_iyr(self) -> bool:
        return self.iyr is not None and \
            len(self.iyr) == 4 and \
            self.iyr.isdigit() and \
            2010 <= int(self.iyr) <= 2020

    def is_valid_eyr(self) -> bool:
        return self.eyr is not None and \
            len(self.eyr) == 4 and \
            self.eyr.isdigit() and \
            2020 <= int(self.eyr) <= 2030

    def is_valid_hgt(self) -> bool:
        if self.hgt is None:
            return False
        if self.hgt[:-2].isdigit():
            if self.hgt[-2:] == 'cm':
                return 150 <= int(self.hgt[:-2]) <= 193
            elif self.hgt[-2:] == 'in':
                return 59 <= int(self.hgt[:-2]) <= 76
        return False

    def is_valid_hcl(self) -> bool:
        return self.hcl is not None and \
            self.hcl[0] == '#' and \
            len(self.hcl) == 7 and \
            is_hex(self.hcl[1:])

    def is_valid_ecl(self) -> bool:
        return self.ecl is not None and \
            self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def is_valid_pid(self) -> bool:
        return self.pid is not None and \
            len(self.pid) == 9 and \
            self.pid.isdigit()

    def is_valid(self) -> bool:
        return self.is_valid_byr() and \
            self.is_valid_iyr() and \
            self.is_valid_eyr() and \
            self.is_valid_hgt() and \
            self.is_valid_hcl() and \
            self.is_valid_ecl() and \
            self.is_valid_pid()

    def parse(self, txt: str) -> None:
        fields = txt.rsplit()
        for field in fields:
            tmp = field.split(':')
            name = tmp[0]
            value = tmp[1]
            if name == 'byr':
                self.byr = value
            elif name == 'iyr':
                self.iyr = value
            elif name == 'eyr':
                self.eyr = value
            elif name == 'hgt':
                self.hgt = value
            elif name == 'hcl':
                self.hcl = value
            elif name == 'ecl':
                self.ecl = value
            elif name == 'pid':
                self.pid = value


def is_hex(string: str) -> bool:
    for c in string:
        if c not in '1234567890abcdefABCDEF':
            return False
    return True


def load(path: str) -> List[Passport]:
    result = []
    passport_txt = ''
    f = open(path)
    for line in f:
        if line == '\n':
            passport = Passport()
            passport.parse(passport_txt)
            result.append(passport)
            passport_txt = ''
        else:
            passport_txt += line

    if len(passport_txt) != 0:
        passport = Passport()
        passport.parse(passport_txt)
        result.append(passport)

    return result


if __name__ == '__main__':
    test_passports = load('04/test_input.txt')
    print('Test01')
    expected_results = [True, False, True, False]
    for i in range(len(expected_results)):
        print(
            f'Passport {i} - {test_passports[i].contains_all_fields()} - expected {expected_results[i]}')

    print('\nTask01')
    passports = load('04/input.txt')
    counter = 0
    for passport in passports:
        if passport.contains_all_fields():
            counter += 1
    print(counter)

    print('\nTask02')
    counter = 0
    for passport in passports:
        if passport.is_valid():
            counter += 1
    print(counter)
