from typing import Dict, Tuple, List, Set
import re

Rules = Dict[str, Tuple[int, int, int, int]]
Ticket = List[int]


def load_data(path: str) -> Tuple[Rules, Ticket, List[Ticket]]:
    f = open(path)
    rules = dict()
    line = f.readline()
    while line != '\n':
        m = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', line)
        if m is not None:
            rules[m[1]] = (int(m[2]), int(m[3]), int(m[4]), int(m[5]))
        line = f.readline()

    f.readline()
    my_ticket = to_int_list(f.readline())

    f.readline()
    f.readline()
    tickets = []
    for line in f.read().splitlines():
        tickets.append(to_int_list(line))

    return rules, my_ticket, tickets


def to_int_list(string: str) -> List[int]:
    result = []
    for n in string.split(','):
        result.append(int(n))
    return result


# returns: True if value satisfy any of rules
def satisfy_any(value: int, rules: Rules) -> bool:
    for f1, t1, f2, t2 in rules.values():
        if f1 <= value <= t1 or f2 <= value <= t2:
            return True
    return False


# returns: names of fields that can be at specified position in the ticket
def can_be(position: int, tickets: List[Ticket], rules: Rules) -> Set[str]:
    result = set()
    for rule, (f1, t1, f2, t2) in rules.items():
        can = True
        for ticket in tickets:
            if not (f1 <= ticket[position] <= t1 or f2 <= ticket[position] <= t2):
                can = False
                break
        if can:
            result.add(rule)
    return result


# returns: list, where items are lists of possible field names for coresponding position
def get_posibilities(tickets: List[Ticket], rules: Rules) -> List[Set[str]]:
    result = []
    for i in range(len(tickets[0])):
        result.append(can_be(i, tickets, rules))
    return result


# returns: names of fields in their correct order
def get_names(posibilities: List[Set[str]]) -> List[str]:
    tt = sort_by_length(posibilities)
    result = []
    for p in posibilities:
        result.append(p.pop())
        for p2 in posibilities:
            p2.discard(result[-1])
    result = translate(result, tt)
    return result


# sorts list based on length of sets
# reutrns: table with old indexes
def sort_by_length(posibilities: List[Set[str]]) -> List[int]:
    p_copy = posibilities.copy()
    posibilities.sort()
    translation_table = []
    for p in p_copy:
        for i in range(len(posibilities)):
            if p is posibilities[i]:
                translation_table.append(i)
                break
    return translation_table


# returns: list with field names in correct order according to translation table
def translate(names: List[str], translation_table: List[int]) -> List[str]:
    return [names[translation_table[i]] for i in range(len(names))]


def solve(input_path: str) -> None:
    rules, my_ticket, tickets = load_data(input_path)

    error_rate = 0
    invalid_ticket_indexes = []
    for i, ticket in enumerate(tickets):
        for value in ticket:
            if not satisfy_any(value, rules):
                error_rate += value
                invalid_ticket_indexes.append(i)
    invalid_ticket_indexes.reverse()
    for i in invalid_ticket_indexes:
        tickets.pop(i)
    print('Error rate:', error_rate)

    posibilities = get_posibilities(tickets, rules)
    names = get_names(posibilities)
    multiplication = 1
    for i, n in enumerate(names):
        if n.startswith('departure'):
            multiplication *= my_ticket[i]
    print('Multiplication:', multiplication)


if __name__ == '__main__':
    solve('16/input.txt')
