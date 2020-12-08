from typing import List, Tuple, Set, Optional

Instruction = Tuple[str, int]


def load_instructions(path: str) -> List[Instruction]:
    f = open(path)
    result = []
    for line in f.readlines():
        ins, val = line.split()
        result.append((ins, int(val)))
    return result


# returns: reached the program end without looping?, accumulatro val at the end of program or at the begining of a loop
def run(instructions) -> Tuple[bool, int]:
    visited_lines: Set[int] = set()
    accumulator = 0
    ip = 0  # instruction pointer

    while ip not in visited_lines and ip < len(instructions):
        visited_lines.add(ip)
        ins, val = instructions[ip]
        if ins == 'acc':
            accumulator += val
            ip += 1
        elif ins == 'jmp':
            ip += val
        elif ins == 'nop':
            ip += 1
        else:
            print(f'{ip}: unknown instruction "{ins}"')

    return ip == len(instructions), accumulator


def repair_run(instructions: List[Instruction]) -> Optional[int]:
    for i in range(len(instructions)):
        ins, val = instructions[i]

        if ins == 'acc':
            continue

        # try repair
        if ins == 'jmp':
            instructions[i] = 'nop', val
        elif ins == 'nop':
            instructions[i] = 'jmp', val

        end, res = run(instructions)
        if end:
            return res
        else:
            instructions[i] = ins, val
    return None


if __name__ == '__main__':
    print('Test01')
    test_instructions = load_instructions('08/test_input.txt')
    print('Accumulator value at loop: ', run(test_instructions)[1])

    print('\nTask01')
    instructions = load_instructions('08/input.txt')
    print('Accumulator value at loop: ', run(instructions)[1])

    print('\nTest02')
    print('Accumulator value after repair: ', repair_run(test_instructions))

    print('\nTask02')
    print('Accumulator value after repair: ', repair_run(instructions))
