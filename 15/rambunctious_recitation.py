from typing import List, Dict


def play(number_list: List[int], n: int) -> int:
    cache: Dict[int, int] = dict(
        [(number_list[i], i) for i in range(0, len(number_list) - 1)])
    prev = number_list[-1]
    for i in range(len(number_list) - 1, n - 1):
        last_index = cache.get(prev)
        cache[prev] = i
        if last_index is None:
            prev = 0
        else:
            prev = i - last_index
    return prev


if __name__ == '__main__':
    print('Test play')
    numbers = [0, 3, 6]
    print(play(numbers, 10))

    print('Play')
    numbers = [0, 6, 1, 7, 2, 19, 20]
    print('2020:', play(numbers, 2020))
    print('30 000 000:', play(numbers, 30000000))
