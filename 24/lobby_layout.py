from typing import Tuple, Set, List, Iterable


def load_pattern(file_path: str) -> List[str]:
    return open(file_path).read().splitlines()


def parse_path(path: str) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    i = 0
    while i < len(path):
        if path[i] == 'e':              # east
            result.append((-2, 0))
            i += 1
        elif path[i] == 's':
            if path[i + 1] == 'e':      # southeast
                result.append((-1, -1))
            else:                       # southwest
                result.append((1, -1))
            i += 2
        elif path[i] == 'w':            # west
            result.append((2, 0))
            i += 1
        else:
            if path[i + 1] == 'e':      # northeast
                result.append((-1, 1))
            else:                       # northwest
                result.append((1, 1))
            i += 2
    return result


def find_tile(path) -> Tuple[int, int]:
    coords = (0, 0)
    for v in path:
        coords = add_tuple(coords, v)
    return coords


def add_tuple(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def init_tiles(pattern: List[str]) -> Set[Tuple[int, int]]:
    black_tiles: Set[Tuple[int, int]] = set()
    for p in map(parse_path, pattern):
        tile_coords = find_tile(p)
        if tile_coords in black_tiles:
            black_tiles.remove(tile_coords)
        else:
            black_tiles.add(tile_coords)
    return black_tiles


def get_adjacen_tiles(tile: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    for v in [(-2, 0), (-1, -1), (1, -1), (2, 0), (1, 1), (-1, 1)]:
        yield add_tuple(tile, v)


def count_adjacent_black_tiles(tile: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> int:
    count = 0
    for t in get_adjacen_tiles(tile):
        if t in black_tiles:
            count += 1
    return count


def step(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    new_black_tiles: Set[Tuple[int, int]] = set()
    adjecent_white_tiles: Set[Tuple[int, int]] = set()

    for bt in black_tiles:
        # stays black?
        if 0 < count_adjacent_black_tiles(bt, black_tiles) <= 2:
            new_black_tiles.add(bt)
        # add adjacent tiles
        adjecent_white_tiles.update(get_adjacen_tiles(bt))
    # remove black tiles
    adjecent_white_tiles.difference_update(black_tiles)

    for wt in adjecent_white_tiles:
        # becomes black?
        if count_adjacent_black_tiles(wt, black_tiles) == 2:
            new_black_tiles.add(wt)

    return new_black_tiles


def solve(file_path: str, name: str) -> None:
    print()
    print(name)

    pattern = load_pattern(file_path)
    black_tiles = init_tiles(pattern)
    print('Day 0:', len(black_tiles))

    for _ in range(100):
        black_tiles = step(black_tiles)

    print('Day 100:', len(black_tiles))


if __name__ == '__main__':
    solve('24/test_input.txt', 'Test')
    solve('24/input.txt', 'Task')
