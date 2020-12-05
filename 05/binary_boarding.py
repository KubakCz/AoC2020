from typing import List, Tuple


Seat = Tuple[int, int]  # row, col


def parse(seat: str) -> Seat:
    row = 0
    col = 0

    # row
    n = 1
    for i in range(6, -1, -1):
        if seat[i] == 'B':
            row += n
        n *= 2

    # col
    n = 1
    for i in range(9, 6, -1):
        if seat[i] == 'R':
            col += n
        n *= 2

    return row, col


def load(path: str) -> List[Seat]:
    result = []
    f = open(path)
    for line in f:
        result.append(parse(line))
    return result


def seat_id(seat: Seat) -> int:
    return seat[0] * 8 + seat[1]


def missing_id(sorted_ids: List[int]) -> int:
    for i in range(1, len(sorted_ids)):
        if sorted_ids[i] - sorted_ids[i - 1] != 1:
            return sorted_ids[i] - 1
    return -1


if __name__ == '__main__':
    print('Test01')
    for str_seat in ['BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']:
        seat = parse(str_seat)
        print(f'{str_seat} - {seat}, {seat_id(seat)}')

    print('\nTask01')
    seats = load('05/input.txt')
    ids = [seat_id(seat) for seat in seats]
    ids.sort()
    print(f'Max id: {ids[-1]}')

    print('\nTask02')
    print(f'Missing id: {missing_id(ids)}')
