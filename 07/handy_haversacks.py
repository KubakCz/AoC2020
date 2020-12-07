from typing import Dict, Tuple, Set


# returns: bag color, dict of contained bags and their counts
def parse_line(line: str) -> Tuple[str, Dict[str, int]]:
    s = line.split()
    bag = s[0] + ' ' + s[1]  # eg. 'light red'

    contains = dict()
    i = 4
    while i < len(s):
        if s[i] == 'no':
            break
        count = int(s[i])  # eg. '1'
        name = s[i + 1] + ' ' + s[i + 2]  # eg. 'bright white'
        contains[name] = count
        i += 4  # +4 words (1 bright white bag,)

    return bag, contains


# returns: key: bag color, value: dict of contained bags and their counts
def load_bags(path: str) -> Dict[str, Dict[str, int]]:
    f = open(path)
    result = dict()
    for line in f.readlines():
        bag, contains = parse_line(line)
        result[bag] = contains
    return result


# returns: key: bag color, value: set of bag colors, that contains the bag
def can_be_in(bags: Dict[str, Dict[str, int]]) -> Dict[str, Set[str]]:
    result: Dict[str, Set[str]] = dict()
    for bag, contains in bags.items():
        for inside_bag in contains:
            if inside_bag in result.keys():
                result[inside_bag].add(bag)
            else:
                result[inside_bag] = set([bag])
    return result


# returns: set of outer bags, that 'bag' can be carried in.
def get_outer_bags(bag: str, can_be_in_dict: Dict[str, Set[str]]) -> Set[str]:
    # dfs
    result: Set[str] = set()
    stack = [bag]

    while len(stack) > 0:
        current = stack.pop()
        for b in can_be_in_dict.get(current, set()):
            if b not in result:
                result.add(b)
                stack.append(b)

    return result


def get_inside_bag_count(bag: str, bag_dict: Dict[str, Dict[str, int]]) -> int:
    return get_inside_bag_count_rec(bag, bag_dict, dict())


def get_inside_bag_count_rec(bag: str, bag_dict: Dict[str, Dict[str, int]], inside_bags: Dict[str, int]) -> int:
    total = 0
    for inside_bag, val in bag_dict[bag].items():
        total += val
        if inside_bag not in inside_bags.keys():
            inside_count = get_inside_bag_count_rec(
                inside_bag, bag_dict, inside_bags)
            total += inside_count * val
        else:
            total += inside_bags[inside_bag] * val
    inside_bags[bag] = total
    return total


if __name__ == '__main__':
    bag = 'shiny gold'

    print('Test01')
    test_bag_dict = load_bags('07/test_input.txt')
    print('\nBags: ', test_bag_dict)
    test_can_be_in_dict = can_be_in(test_bag_dict)
    print('\nx can be in y, z...: ', test_can_be_in_dict)
    test_outer_bags = get_outer_bags(bag, test_can_be_in_dict)
    print('\nShiny gold bag - outermost bags: ', test_outer_bags)

    print('\nTask01')
    bag_dict = load_bags('07/input.txt')
    can_be_in_dict = can_be_in(bag_dict)
    outer_bags = get_outer_bags(bag, can_be_in_dict)
    print('Shiny gold bag outer bag color count: ', len(outer_bags))

    print('\nTest02')
    print('Inside bag count: ', get_inside_bag_count(bag, test_bag_dict))

    print('\nTask02')
    print('Inside bag count: ', get_inside_bag_count(bag, bag_dict))
