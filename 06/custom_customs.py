from typing import List, Set


def load(path: str) -> List[List[str]]:
    result = []
    group: List[str] = []
    f = open(path)
    for line in f:
        if line == '\n':
            result.append(group)
            group = []
        else:
            group.append(line[:-1])

    if len(group) != 0:
        result.append(group)

    return result


def group_anyone(answers: List[List[str]]) -> List[Set[str]]:
    result = []
    for group in answers:
        group_res = set()
        for ans in group:
            group_res.update(set(ans))
        result.append(group_res)

    return result


def group_everyone(answers: List[List[str]]) -> List[Set[str]]:
    result = []
    for group in answers:
        group_res = set(group[0])
        for i in range(1, len(group)):
            group_res.intersection_update(set(group[i]))
        result.append(group_res)
    return result


if __name__ == '__main__':
    answers = load('06/input.txt')

    print('Task01')
    answers_groups_anyone = group_anyone(answers)
    total = sum([len(ans) for ans in answers_groups_anyone])
    print(f'Total: {total}')

    print('\nTask02')
    answers_groups_everyone = group_everyone(answers)
    total = sum([len(ans) for ans in answers_groups_everyone])
    print(f'Total: {total}')
