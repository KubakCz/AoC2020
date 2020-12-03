from typing import List, Tuple

Map = List[List[bool]]


class TreeMap:
    def __init__(self, map_file: str) -> None:
        self.map = self.load_map(map_file)

    def load_map(self, map_file: str) -> Map:
        result_map = []
        f = open(map_file)
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            result_map.append([(c == '#') for c in line])
        return result_map

    def print_map(self) -> None:
        for row in self.map:
            for col in row:
                print('#' if col else '.', end='')
            print()
        print()

    def get(self, row: int, col: int) -> bool:
        row = row % len(self.map)
        col = col % len(self.map[row])
        return self.map[row][col]

    def tree_counter(self, row_step: int, col_step: int) -> int:
        row = 0
        col = 0
        counter = 0
        while row < len(self.map):
            if self.get(row, col):
                counter += 1
            row += row_step
            col += col_step
        return counter


if __name__ == '__main__':
    print('Test01')
    test_t_map = TreeMap('03/test_input.txt')
    test_t_map.print_map()
    print(f'\nTrees in the path: {test_t_map.tree_counter(1, 3)}')

    print('\nTask01')
    t_map = TreeMap('03/input.txt')
    print(f'Trees in the path: {t_map.tree_counter(1, 3)}')

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]  # row_step, col_step
    print('\ntest02')
    for slope in slopes:
        print(f'{slope}: {test_t_map.tree_counter(slope[0], slope[1])}')

    print('\nTask02')
    mult = 1
    for slope in slopes:
        res = t_map.tree_counter(slope[0], slope[1])
        print(f'{slope}: {res}')
        mult *= res
    print(f'Multiplication: {mult}')
