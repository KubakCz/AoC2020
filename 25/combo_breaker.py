from typing import Tuple

subject = 7
mod = 20201227


def load_public_keys(file_path: str) -> Tuple[int, int]:
    f = open(file_path)
    return int(f.readline()), int(f.readline())


def transform(subject: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= mod
    return value


def find_loop_size(subject: int, public_key: int) -> int:
    loop_size = 0
    value = 1
    while value != public_key:
        value = (value * subject) % mod
        loop_size += 1
    return loop_size


def solve(file_path: str, name: str) -> None:
    print()
    print(name)

    pka, pkb = load_public_keys(file_path)
    lsa = find_loop_size(subject, pka)
    ek = transform(pkb, lsa)
    print("Encryption key:", ek)


if __name__ == '__main__':
    solve("25/test_input.txt", "Test")
    solve("25/input.txt", "Task")
