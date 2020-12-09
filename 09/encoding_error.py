from typing import List, Deque, Tuple
from bisect import bisect_left
from collections import deque


def load_numbers(path: str) -> List[int]:
    result = []
    f = open(path)
    for line in f.readlines():
        result.append(int(line))
    return result


# modified 'find_entries(...)' from the first day
# return: true if two numbers from 'sorted_list' adds to 'sum'
def sum_exists(sum: int, sorted_list: List[int]) -> bool:
    i = 0
    j = len(sorted_list) - 1
    tmp_sum = sorted_list[i] + sorted_list[j]
    while i < j and tmp_sum != sum:
        if tmp_sum < sum:
            i += 1
        else:
            j -= 1
        tmp_sum = sorted_list[i] + sorted_list[j]

    return tmp_sum == sum


def add_remove(sorted_list: List[int], remove_val: int, add_val: int) -> None:
    # removes one value and adds another
    # avoids adding and removing values from the list
    # removed value must be in the list!
    sl = sorted_list
    index = bisect_left(sl, remove_val)
    # swap values
    sl[index] = add_val

    # move new value to the corect place
    while index > 0 and sl[index] < sl[index - 1]:
        sl[index], sl[index - 1] = sl[index - 1], sl[index]
        index -= 1
    while index < len(sl) - 1 and sl[index] > sl[index + 1]:
        sl[index], sl[index + 1] = sl[index + 1], sl[index]
        index += 1


def first_not_sum_index(numbers: List[int], preamble_length: int) -> int:
    # using red-black tree or something like that would be faster
    # (search, insert, delete in O(log n))
    # using sorted list - search O(log n), insert, delete O(n)
    buffer = numbers[:preamble_length]
    buffer.sort()
    for i in range(preamble_length, len(numbers)):
        if not sum_exists(numbers[i], buffer):
            return i
        add_remove(buffer, numbers[i - preamble_length], numbers[i])
    return -1


# returns sublist of 'numbers', where sum(sublist) == 'total'
def find_contiguous_sublist(total: int, numbers: List[int]) -> List[int]:
    subque: Deque[int] = deque()
    subque_sum = 0
    for n in numbers:
        subque.append(n)
        subque_sum += n
        while subque_sum > total:
            subque_sum -= subque.popleft()
        if subque_sum == total and len(subque) > 1:
            return list(subque)
    return []


def min_max(numbers: List[int]) -> Tuple[int, int]:
    mi = numbers[0]
    ma = numbers[0]
    for n in numbers:
        if n < mi:
            mi = n
        if n > ma:
            ma = n
    return mi, ma


if __name__ == '__main__':
    print('Test01')
    test_numbers = load_numbers('09/test_input.txt')
    test_index = first_not_sum_index(test_numbers, 5)
    print(f'index: {test_index}, val: {test_numbers[test_index]}')

    print('\nTask01')
    numbers = load_numbers('09/input.txt')
    index = first_not_sum_index(numbers, 25)
    print(f'index: {index}, val: {numbers[index]}')

    print('\nTest02')
    test_sublist = find_contiguous_sublist(
        test_numbers[test_index], test_numbers)
    mi, ma = min_max(test_sublist)
    print(f'min max sum: {mi + ma}')

    print('\nTask02')
    sublist = find_contiguous_sublist(numbers[index], numbers)
    mi, ma = min_max(sublist)
    print(f'min max sum: {mi + ma}')
