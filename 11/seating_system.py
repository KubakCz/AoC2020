from typing import List, Callable


EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'


class SeatMap:
    def __init__(self):
        self.seats: List[List[str]] = [[]]

    def load_seats(self, path: str) -> None:
        self.seats = [[c for c in line]
                      for line in open(path).read().splitlines()]

    def print_seats(self) -> None:
        for row in self.seats:
            for col in row:
                print(col, end='')
            print()

    def get(self, row: int, col: int) -> str:
        if row < 0 or row >= len(self.seats) or col < 0 or col >= len(self.seats[0]):
            return EMPTY
        return self.seats[row][col]

    def get_seat_in_direction(self, row: int, col: int, row_step: int, col_step: int) -> str:
        row += row_step
        col += col_step
        seat = self.get(row, col)
        while seat == FLOOR:
            row += row_step
            col += col_step
            seat = self.get(row, col)
        return seat

    def adjacent_occupied_seats(self, row: int, col: int) -> int:
        total = 0
        for dr, dc in [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]:
            if self.get(row + dr, col + dc) == OCCUPIED:
                total += 1
        return total

    def direction_occupied_seats(self, row: int, col: int) -> int:
        total = 0
        for dr, dc in [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]:
            if self.get_seat_in_direction(row, col, dr, dc) == OCCUPIED:
                total += 1
        return total

    # returns number of chnages in the map

    def step(self) -> int:
        change_counter = 0
        new_seats = []
        for row in range(len(self.seats)):
            new_row = []
            for col in range(len(self.seats[0])):
                if self.get(row, col) == EMPTY and \
                        self.adjacent_occupied_seats(row, col) == 0:
                    new_row.append(OCCUPIED)
                    change_counter += 1
                elif self.get(row, col) == OCCUPIED and \
                        self.adjacent_occupied_seats(row, col) >= 4:
                    new_row.append(EMPTY)
                    change_counter += 1
                else:
                    new_row.append(self.get(row, col))
            new_seats.append(new_row)
        self.seats = new_seats
        return change_counter

    def step2(self) -> int:
        change_counter = 0
        new_seats = []
        for row in range(len(self.seats)):
            new_row = []
            for col in range(len(self.seats[0])):
                if self.get(row, col) == EMPTY and \
                        self.direction_occupied_seats(row, col) == 0:
                    new_row.append(OCCUPIED)
                    change_counter += 1
                elif self.get(row, col) == OCCUPIED and \
                        self.direction_occupied_seats(row, col) >= 5:
                    new_row.append(EMPTY)
                    change_counter += 1
                else:
                    new_row.append(self.get(row, col))
            new_seats.append(new_row)
        self.seats = new_seats
        return change_counter

    def simulate(self, step_method: Callable[['SeatMap'], int]) -> None:
        while step_method(self) > 0:
            pass

    def occupied_seats_count(self) -> int:
        counter = 0
        for row in self.seats:
            for col in row:
                if col == OCCUPIED:
                    counter += 1
        return counter


if __name__ == "__main__":
    print('Test01')
    test_seats = SeatMap()
    test_seats.load_seats('11/test_input.txt')
    test_seats.print_seats()
    print()
    test_seats.step()
    test_seats.print_seats()
    print()
    test_seats.step()
    test_seats.print_seats()
    print('\nSimulating...')
    test_seats.simulate(SeatMap.step)
    print('Occupied seats: ', test_seats.occupied_seats_count())

    print('\nTask01')
    seats = SeatMap()
    seats.load_seats('11/input.txt')
    seats.simulate(SeatMap.step)
    print('Occupied seats: ', seats.occupied_seats_count())

    print('\nTest02')
    test_seats = SeatMap()
    test_seats.load_seats('11/test_input.txt')
    test_seats.simulate(SeatMap.step2)
    print('Occupied seats: ', test_seats.occupied_seats_count())

    print('\nTask02')
    seats = SeatMap()
    seats.load_seats('11/input.txt')
    seats.simulate(SeatMap.step2)
    print('Occupied seats: ', seats.occupied_seats_count())
