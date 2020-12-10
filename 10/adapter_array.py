from typing import List, Tuple


def load_adapters(path: str) -> List[int]:
    result = []
    f = open(path)
    for line in f.readlines():
        result.append(int(line))
    return result


def jolt_differences(sorted_adapters) -> Tuple[int, int, int]:
    diffs = [0, 0, 1]   # one for device
    diffs[sorted_adapters[0] - 1] += 1  # +1 for the first adapter
    for i in range(1, len(sorted_adapters)):
        diffs[sorted_adapters[i] - sorted_adapters[i - 1] - 1] += 1
    return diffs[0], diffs[1], diffs[2]


def split_adapters(sorted_adapters: List[int]) -> List[List[int]]:
    # split adapters into groups,
    # between each group end and beginnig is 3 jolt difference
    result = [[0]]
    for a in sorted_adapters:
        if a - result[-1][-1] == 3:
            result.append([a])
        else:
            result[-1].append(a)
    return result


# works only with 1 or 3 differences in jolts - this is true for
# both test inputs and puzzle input
def adapter_combinations(sorted_adapters: List[int]) -> int:
    # find groups of adapters with differences less then 3,
    # where are at least 3 adapters
    # eg. 0 - [3, 4, 5, 6] - 9...
    groups = split_adapters(sorted_adapters)
    max_group_size = 0
    for group in groups:
        if len(group) > max_group_size:
            max_group_size = len(group)

    # on index i is number of combinations for group of size n
    combinations = [1, 1, 1, 2, 4, 7]
    # this should work, but there werent any groups bigger then 5 in inputs
    # so this part could be excluded
    while len(combinations) < max_group_size:
        # combinations[n] =
        #     2 * combinations[n-2] + 2 * combinations[n-3] + combinations[n-4]
        # for n > 5
        combinations.append(
            2*combinations[-2] + 2*combinations[-3] + combinations[-4])

    total_combinations = 1
    for group in groups:
        total_combinations *= combinations[len(group)]
    return total_combinations


if __name__ == "__main__":
    print('Test01')
    test_adapters1 = load_adapters('10/test_input1.txt')
    test_adapters1.sort()
    print(jolt_differences(test_adapters1))
    test_adapters2 = load_adapters('10/test_input2.txt')
    test_adapters2.sort()
    print(jolt_differences(test_adapters2))

    print('\nTask01')
    adapters = load_adapters('10/input.txt')
    adapters.sort()
    diffs = jolt_differences(adapters)
    print('diff 1 * diff 3 = ', diffs[0] * diffs[2])

    print('\nTest02')
    print('test_input01 combinations: ', adapter_combinations(test_adapters1))
    print('test_input02 combinations: ', adapter_combinations(test_adapters2))

    print('\nTask02')
    print('combinations: ', adapter_combinations(adapters))
