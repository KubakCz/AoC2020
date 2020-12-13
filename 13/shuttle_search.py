from typing import Tuple, List, Optional
from math import inf

# return: now, bus ids


def load_buses(path: str) -> Tuple[int, List[int]]:
    f = open(path)
    now = int(f.readline())
    buses = []
    for bus_id in f.readline().split(','):
        if bus_id == 'x':
            buses.append(0)
        else:
            buses.append(int(bus_id))
    return now, buses


# return: time until next depart
def departs_in(bus_id: int, now: int) -> float:
    return bus_id - now % bus_id if bus_id != 0 else inf


# return: (bus id, waiting time)
def first_departing_bus(buses: List[int], now: int) -> Tuple[int, float]:
    departs_list = [departs_in(bus_id, now) for bus_id in buses]
    min_index = 0
    for i in range(1, len(buses)):
        if departs_list[i] < departs_list[min_index]:
            min_index = i
    return buses[min_index], departs_list[min_index]


# a x congruent b mod n ~> x congruent c mod m
# reutrns: c, m
def solve_congruence(a: int, b: int, n: int) -> Optional[Tuple[int, int]]:
    prev_a = n
    prev_b = 0
    a %= n
    b %= n
    while a > 1:
        prev_b, b = b, (prev_b - (prev_a // a) * b) % n
        prev_a, a = a, prev_a % a

    if a == 1:
        return b, n
    # a == 0:
    if b == 0:
        return prev_b // prev_a, n // prev_a
    return None


# system of 'x congruent b mod n' ~> x congruent c mod m
# input: List of (b, n)
# return: c, m
def solve_congruence_system(congruences: List[Tuple[int, int]]) \
        -> Optional[Tuple[int, int]]:
    # x congruent b mod n <=> x = nk + b
    #                             ^    ^
    #                             k    l
    k = congruences[0][1]
    l = congruences[0][0] % k
    for b, n in congruences:
        tmp = solve_congruence(k, b - l, n)
        if tmp is None:
            return None
        l += tmp[0] * k
        k *= tmp[1]

    return l, k


def buses_to_congruece_system(buses: List[int]) -> List[Tuple[int, int]]:
    conguences = []
    for i in range(len(buses)):
        if buses[i] != 0:
            conguences.append((-i, buses[i]))
    return conguences


def congruence_test() -> None:
    print()
    print('Congruence test')
    print(solve_congruence(1, 4, 7))            # ~> (4, 7)
    print(solve_congruence(7, -1, 13))          # ~> (11, 13)
    print(solve_congruence(68799, 761, 59))     # ~> (46, 59)
    print(solve_congruence(68794, 761, 58))     # ~> None
    print(solve_congruence(130, 150, 232))      # ~> (19, 116)

    print(solve_congruence_system([(7, 27), (-3, 11)]))  # ~> (250, 297)

    print(solve_congruence_system([(0, 3), (2, 5), (3, 7), (4, 11), (9, 13)]))
    # ~> (6 912, 15 015)

    print(solve_congruence_system(
        buses_to_congruece_system([67, 7, 0, 59, 61])))
    # ~> (1 261 476, xxx)


def task(name: str, file_path: str) -> None:
    print()
    print(name)
    now, buses = load_buses(file_path)
    bus, waiting_time = first_departing_bus(buses, now)
    print(f'Bus: {bus}, departs in: {waiting_time}')
    print(f'Answer 1: {bus * waiting_time}')

    congruences = buses_to_congruece_system(buses)
    solution = solve_congruence_system(congruences)
    print('Answer 2: timestamp:', solution[0]
          if solution is not None else None)


if __name__ == "__main__":
    congruence_test()
    task('Test', '13/test_input.txt')
    task('Task', '13/input.txt')
