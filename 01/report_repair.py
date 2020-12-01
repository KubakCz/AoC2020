from typing import List, Tuple, Optional


def load(input_file: str) -> List[int]:
    input_list = []
    f = open(input_file)
    for line in f:
        input_list.append(int(line))
    return input_list


def find_entries(entry_sum: int, input_list: List[int]) \
        -> Optional[Tuple[int, int]]:
    if len(input_list) < 2:
        return None

    inputs = sorted(input_list)
    i = 0
    j = len(inputs) - 1
    tmp_sum = inputs[i] + inputs[j]
    while i < j and tmp_sum != entry_sum:
        if tmp_sum < entry_sum:
            i += 1
        else:
            j -= 1
        tmp_sum = inputs[i] + inputs[j]

    return (inputs[i], inputs[j]) if i < j else None


def find_entries3(entry_sum: int, input_list: List[int]) \
        -> Optional[Tuple[int, int, int]]:
    inputs = sorted(input_list)
    for i in range(len(input_list)):
        tmp_result = find_entries(entry_sum - inputs[i], inputs[i+1:])
        if tmp_result is not None:
            return inputs[i], tmp_result[0], tmp_result[1]
    return None


if __name__ == '__main__':
    print("Test 01")
    result = find_entries(2020, [1721, 979, 366, 299, 675, 1456])
    if result is None:
        print("None - Nok")
    else:
        print(f"{result[0]} + {result[1]} " +
              ("==" if result[0] + result[1] == 2020 else "!=") + " 2020")

    print("\nTest 02")
    result = find_entries(2020, [1721, 979, 366, 675, 1456])
    if result is None:
        print("None - ok")
    else:
        print(f"{result[0]} * {result[1]} " +
              ("==" if result[0] * result[1] == 2020 else "!=") + "2020")

    print("\nPuzzle 01:")
    input_list = load("input1.txt")
    result = find_entries(2020, input_list)
    if result is None:
        print(None)
    else:
        print(f"{result[0]} * {result[1]} = {result[0] * result[1]}")

    print("\nTest 03")
    result3 = find_entries3(2020, [1721, 979, 366, 299, 675, 1456])
    if result3 is None:
        print("None - Nok")
    else:
        print(f"{result3[0]} + {result3[1]} + {result3[2]} " +
              ("==" if result3[0] + result3[1] + result3[2] == 2020 else "!=") + " 2020")

    print("\nTest 02")
    result3 = find_entries3(2020, [1721, 979, 299, 675, 1456])
    if result3 is None:
        print("None - ok")
    else:
        print(f"{result3[0]} + {result3[1]} + {result3[2]}" +
              ("==" if result3[0] + result3[1] + result3[2] == 2020 else "!=") + " 2020")

    print("\nPuzzle 02:")
    input_list = load("input1.txt")
    result3 = find_entries3(2020, input_list)
    if result3 is None:
        print(None)
    else:
        print(
            f"{result3[0]} * {result3[1]} * {result3[2]} = {result3[0] * result3[1] * result3[2]}")
