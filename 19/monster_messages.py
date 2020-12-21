from typing import Optional, List, Iterator, Tuple, Set, Dict


class Rule:
    def __init__(self, rule: str):
        self.letter, self.references = Rule.parse(rule)

    @staticmethod
    def parse(rule: str) -> Tuple[Optional[str], List[List[int]]]:
        if rule[0] == '"':
            return rule[1], []
        result: List[List[int]] = [[]]
        for t in rule.split():
            if t == '|':
                result.append([])
            else:
                result[-1].append(int(t))
        return None, result


def load_input(path: str) -> Tuple[Dict[int, Rule], List[str]]:
    rules = dict()
    messages = []

    f = open(path)
    line = f.readline()
    while line != '\n':
        tmp = line.split(": ")
        rules[int(tmp[0])] = Rule(tmp[1])
        line = f.readline()
    for line in f.read().splitlines():
        messages.append(line)

    return rules, messages


# return: True, if message matches rule 'n'
def matches(message: str, rules: Dict[int, Rule], n: int) -> bool:
    for l in matches_rec(message, 0, rules, n):
        if len(message) == l:
            return True
    return False


# returns: list of numbers of matched characters from message
# from 'start' index or empty list, if no match
# n: rule that should be matched
def matches_rec(message: str, start: int, rules: Dict[int, Rule], n: int) \
        -> List[int]:
    if start >= len(message):
        return []

    rule = rules[n]
    if rule.letter is not None:
        if rule.letter == message[start]:
            return [start + 1]
        return []

    last_matched: List[int] = []
    for r in rule.references:
        last_matched.extend(matches_rules(message, start, rules, r))

    return last_matched


# return: list of numbers of matched characters from message
# from 'start' index or empty list, if no match
# rules_to_match: list of rules, that have to match after each other
def matches_rules(message: str, start: int,
                  rules: Dict[int, Rule],
                  rules_to_match: List[int]) -> List[int]:
    starts = [start]
    for r in rules_to_match:
        new_starts = []
        for s in starts:
            last_matched = matches_rec(message, s, rules, r)
            new_starts.extend(last_matched)
        starts = new_starts
    return starts


def solve(file_path: str, name: str):
    print()
    print(name)

    rules, messages = load_input(file_path)

    counter = 0
    for m in messages:
        if matches(m, rules, 0):
            counter += 1
    print('Messages that match rule 0:', counter)

    rules[8] = Rule('42 | 42 8')
    rules[11] = Rule('42 31 | 42 11 31')
    counter = 0
    for m in messages:
        if matches(m, rules, 0):
            counter += 1
    print('Messages that match rule 0 after rule changes:', counter)


if __name__ == '__main__':
    solve('19/test_input.txt', 'Test01')
    solve('19/test_input2.txt', 'Test02')
    solve('19/input.txt', 'Task')
