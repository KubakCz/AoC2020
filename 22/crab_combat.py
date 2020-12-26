from typing import Tuple, Deque, Set
from collections import deque
import itertools


def load_decks(path: str) -> Tuple[Deque[int], Deque[int]]:
    f = open(path)
    lines = f.read().splitlines()

    i = 1
    p1: Deque[int] = deque()
    while lines[i] != '':
        p1.append(int(lines[i]))
        i += 1

    i += 2
    p2: Deque[int] = deque()
    while len(lines) > i:
        p2.append(int(lines[i]))
        i += 1

    return p1, p2


def combat_step(p1: Deque[int], p2: Deque[int]) -> None:
    p1_card = p1.popleft()
    p2_card = p2.popleft()

    if p1_card > p2_card:
        p1.append(p1_card)
        p1.append(p2_card)
    else:
        p2.append(p2_card)
        p2.append(p1_card)


def play_combat(p1: Deque[int], p2: Deque[int]) -> int:
    while len(p1) > 0 and len(p2) > 0:
        combat_step(p1, p2)
    return 1 if len(p1) != 0 else 2


def rec_combat_step(p1: Deque[int], p2: Deque[int]) -> None:
    p1_card = p1.popleft()
    p2_card = p2.popleft()

    if p1_card <= len(p1) and p2_card <= len(p2):
        winner = play_recursive_combat(
            deque(itertools.islice(p1, 0, p1_card)),
            deque(itertools.islice(p2, 0, p2_card)))
    else:
        winner = 1 if p1_card > p2_card else 2

    if winner == 1:
        p1.append(p1_card)
        p1.append(p2_card)
    else:
        p2.append(p2_card)
        p2.append(p1_card)


def play_recursive_combat(p1: Deque[int], p2: Deque[int]) -> int:
    p1_card_set: Set[Tuple] = set()
    p2_card_set: Set[Tuple] = set()
    while len(p1) > 0 and len(p2) > 0:
        p1_t = tuple(p1)
        p2_t = tuple(p2)
        if p1_t in p1_card_set or p2_t in p2_card_set:
            return 1
        p1_card_set.add(p1_t)
        p2_card_set.add(p2_t)
        rec_combat_step(p1, p2)

    return 1 if len(p1) != 0 else 2


def count_score(deck: Deque[int]) -> int:
    score = 0
    k = 1
    while len(deck) > 0:
        score += k * deck.pop()
        k += 1
    return score


def solve(file_path: str, name: str):
    print()
    print(name)
    p1_deck, p2_deck = load_decks(file_path)

    p1 = p1_deck.copy()
    p2 = p2_deck.copy()
    winner = p1 if play_combat(p1, p2) == 1 else p2
    score = count_score(winner)
    print("Combat score:", score)

    p1 = p1_deck.copy()
    p2 = p2_deck.copy()
    winner = p1 if play_recursive_combat(p1, p2) == 1 else p2
    score = count_score(winner)
    print("Combat score:", score)


if __name__ == '__main__':
    solve('22/test_input.txt', 'Test')
    solve('22/input.txt', 'Task')
