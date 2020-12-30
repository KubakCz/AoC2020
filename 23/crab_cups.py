from typing import List, Optional, Tuple, Iterator
from collections import deque


class Cup:
    def __init__(self, label: int, pred: Optional['Cup'] = None, succ: Optional['Cup'] = None):
        self.label = label
        self.pred = pred
        self.succ = succ


# NOT SAFE TO USE
# functions can easily cycle or break the circle if used incorectly
class CupCircle:
    def __init__(self, cups: List[int]):
        self.current, self.cup_list = CupCircle.create_circle(cups)

    def remove_chunk(self, first: Cup, last: Cup) -> None:
        first.pred.succ = last.succ  # type: ignore
        last.succ.pred = first.pred  # type: ignore

    def add_chunk_after(self, after: Cup, first: Cup, last: Cup) -> None:
        first.pred = after
        last.succ = after.succ
        after.succ = first
        last.succ.pred = last  # type: ignore

    def find(self, label: int) -> Cup:
        return self.cup_list[label - 1]

    def iter(self) -> Iterator[int]:
        yield self.current.label
        current = self.current.succ
        while current != self.current:
            yield current.label  # type: ignore
            current = current.succ  # type: ignore

    @staticmethod
    def create_circle(cups: List[int]) -> Tuple[Cup, List[Cup]]:
        cup_list = [Cup(i + 1) for i in range(len(cups))]

        first = cup_list[cups[0] - 1]
        last = first

        for i in range(1, len(cups)):
            current = cup_list[cups[i] - 1]
            current.pred = last
            last.succ = current
            last = current

        last.succ = first
        first.pred = last
        return first, cup_list


class Cups:
    def __init__(self, cups: str, million: bool = False):
        cup_list = [int(n) for n in cups]
        if million:
            cup_list.extend([n for n in range(len(cup_list) + 1, 1000001)])
        self.cup_circle = CupCircle(cup_list)
        self.max_label = len(cup_list)

    def step(self) -> None:
        removed: List[Cup] = [self.cup_circle.current.succ]  # type: ignore
        removed.append(removed[-1].succ)   # type: ignore
        removed.append(removed[-1].succ)   # type: ignore

        self.cup_circle.remove_chunk(removed[0], removed[-1])

        destination = self.cup_circle.find(
            self.get_destination_label(self.cup_circle.current.label, list(map(lambda c: c.label, removed))))

        self.cup_circle.add_chunk_after(destination, removed[0], removed[-1])
        self.cup_circle.current = self.cup_circle.current.succ  # type: ignore

    def get_destination_label(self, current: int, removed: List[int]) -> int:
        dest = current - 1
        if dest < 1:
            dest = self.max_label

        while dest in removed:
            dest -= 1
            if dest < 1:
                dest = self.max_label

        return dest

    def simulate(self, n: int) -> None:
        for i in range(n):
            self.step()

    def result_str(self) -> str:
        current = self.cup_circle.current
        self.cup_circle.current = self.cup_circle.find(1)
        result_iter = self.cup_circle.iter()
        next(result_iter)
        result = ''.join(map(str, result_iter))
        self.cup_circle.current = current
        return result

    def __str__(self):
        return ''.join(map(str, self.cup_circle.iter()))


def solve(file_path: str, name: str) -> None:
    print()
    print(name)
    input_str = open(file_path).readline()
    cups = Cups(input_str)
    cups.simulate(100)
    print('Part 1:', cups.result_str())

    m_cups = Cups(input_str, True)
    m_cups.simulate(10000000)

    c1: Cup = m_cups.cup_circle.find(1).succ  # type: ignore
    c2: Cup = c1.succ  # type: ignore
    print(
        f'Part 2: {c1.label} * {c2.label} = {c1.label * c2.label}')


if __name__ == '__main__':
    solve('23/test_input.txt', 'Test')
    solve('23/input.txt', 'Task')
