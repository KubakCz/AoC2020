from typing import Dict, List


class Value:
    lenght = 36

    def __init__(self, val: int):
        self.set_val(val)

    def set_val(self, val: int) -> None:
        self.val: List[int] = []
        for _ in range(Value.lenght):
            self.val.append(val % 2)
            val //= 2

    def get_val(self) -> List[int]:
        k = 1
        result = [0]
        for bit in self.val:
            if bit == 1:
                result = list(map(lambda x: x + k, result))
            if bit == -1:
                result += list(map(lambda x: x + k, result))
            k *= 2
        return result


class Mask:
    def __init__(self, mask: str):
        self.set_mask(mask)

    def set_mask(self, mask: str) -> None:
        self.mask: List[int] = []
        for bit in mask:
            if bit == '1':
                self.mask.append(1)
            elif bit == '0':
                self.mask.append(0)
            else:
                self.mask.append(-1)
        self.mask.reverse()

    def aply_mask_v1(self, val: Value) -> None:
        for i in range(val.lenght):
            if self.mask[i] != -1:
                val.val[i] = self.mask[i]

    def aply_mask_v2(self, val: Value) -> None:
        for i in range(val.lenght):
            if self.mask[i] != 0:
                val.val[i] = self.mask[i]


def run_v1(path: str) -> Dict[int, int]:
    f = open(path)
    mem: Dict[int, int] = dict()
    for line in f.read().splitlines():
        words = line.split(' = ')
        if words[0] == 'mask':  # mask
            mask = Mask(words[1])
        else:   # mem
            address = (int(words[0][4:-1]))
            val = Value(int(words[1]))
            mask.aply_mask_v1(val)
            mem[address] = val.get_val()[0]
    return mem


def run_v2(path: str) -> Dict[int, int]:
    f = open(path)
    mem: Dict[int, int] = dict()
    for line in f.read().splitlines():
        words = line.split(' = ')
        if words[0] == 'mask':  # mask
            mask = Mask(words[1])
        else:   # mem
            address = Value(int(words[0][4:-1]))
            val = int(words[1])
            mask.aply_mask_v2(address)
            for addr in address.get_val():
                mem[addr] = val
    return mem


def solve(file_path: str, name: str) -> None:
    print()
    print(name)
    print('v1 mem sum:', sum(run_v1(file_path).values()))
    print('v2 mem sum:', sum(run_v2(file_path).values()))


def test() -> None:
    print('\nTest')
    print('v1 mem sum:', sum(run_v1('14/test_input.txt').values()))
    print('v2 mem sum:', sum(run_v2('14/test_input2.txt').values()))


if __name__ == '__main__':
    test()
    solve('14/input.txt', 'Task')
