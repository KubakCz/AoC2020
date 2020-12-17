from typing import Set, Tuple, Dict, Iterator, Callable


def load_input_slice(path: str) -> Set[Tuple[int, int, int, int]]:
    f = open(path)
    coords = set()
    for y, line in enumerate(f.read().splitlines()):
        for x, char in enumerate(line):
            if char == '#':
                coords.add((x, y, 0, 0))
    return coords


def neighbour_gen3() -> Iterator[Tuple[int, int, int, int]]:
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                if x != 0 or y != 0 or z != 0:
                    yield (x, y, z, 0)


def neighbour_gen4() -> Iterator[Tuple[int, int, int, int]]:
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                for w in range(-1, 2):
                    if x != 0 or y != 0 or z != 0 or w != 0:
                        yield (x, y, z, w)


def simulate_step(active_cubes: Set[Tuple[int, int, int, int]],
                  neighbour_gen: Callable[[], Iterator[Tuple[int, int, int, int]]]) \
        -> Set[Tuple[int, int, int, int]]:
    new_active = set()
    active_neighbours: Dict[Tuple[int, int, int, int], int] = dict()
    for x, y, z, w in active_cubes:
        active = 0
        for dx, dy, dz, dw in neighbour_gen():
            neighbour_coord = (x + dx, y + dy, z + dz, w + dw)
            if neighbour_coord in active_cubes:
                active += 1
            else:
                active_neighbours[neighbour_coord] = \
                    active_neighbours.get(neighbour_coord, 0) + 1
        if 2 <= active <= 3:
            new_active.add((x, y, z, w))
    for coord, val in active_neighbours.items():
        if val == 3:
            new_active.add(coord)

    return new_active


def simulate(initial_state: Set[Tuple[int, int, int, int]], n: int,
             neighbour_gen: Callable[[], Iterator[Tuple[int, int, int, int]]]) \
        -> Set[Tuple[int, int, int, int]]:
    state = initial_state.copy()
    for _ in range(n):
        state = simulate_step(state, neighbour_gen)
    return state


def solve(path: str, name: str) -> None:
    print(name)
    init_state = load_input_slice(path)
    final_state = simulate(init_state, 6, neighbour_gen3)
    print('Active cubes 3 dimensional:', len(final_state))
    final_state = simulate(init_state, 6, neighbour_gen4)
    print('Active cubes 4 dimensional:', len(final_state))


if __name__ == '__main__':
    solve('17/test_input.txt', 'Test01')
    solve('17/input.txt', 'Task01')
