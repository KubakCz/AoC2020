from typing import Tuple, List
import re

Policy = Tuple[Tuple[int, int], str]


def parse_line(line: str) -> Tuple[Policy, str]:
    m = re.match(r'(\d+)-(\d+) (.): (\S+)', line)
    return ((int(m[1]), int(m[2])), m[3]), m[4]  # type: ignore


def load(path: str) -> List[Tuple[Policy, str]]:
    result = []
    f = open(path)
    for line in f:
        result.append(parse_line(line))
    return result


def is_valid(policy: Policy, password: str) -> bool:
    min_p, max_p = policy[0]
    letter_p = policy[1]
    letter_count = 0
    for c in password:
        if c == letter_p:
            letter_count += 1
    return min_p <= letter_count <= max_p


def is_valid2(policy: Policy, password: str) -> bool:
    pos1, pos2 = policy[0]
    pos1 -= 1
    pos2 -= 1
    letter = policy[1]
    return (password[pos1] == letter or password[pos2] == letter) and password[pos1] != password[pos2]


if __name__ == '__main__':
    print('Test01')
    for i in ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]:
        policy, passwd = parse_line(i)
        print(i + " -- " + ("valid" if is_valid(policy, passwd) else "not valid"))

    print('\nTask01')
    inputs = load('02/input1.txt')
    counter = 0
    for policy, passwd in inputs:
        if is_valid(policy, passwd):
            counter += 1
    print("Valid passwords: " + str(counter))

    print('\nTest02')
    for i in ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]:
        policy, passwd = parse_line(i)
        print(i + " -- " + ("valid" if is_valid2(policy, passwd) else "not valid"))

    print('\nTask02')
    counter = 0
    for policy, passwd in inputs:
        if is_valid2(policy, passwd):
            counter += 1
    print("Valid passwords: " + str(counter))
