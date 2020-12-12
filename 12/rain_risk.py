from typing import List, Tuple, Callable


def load_instructions(path: str) -> List[Tuple[str, int]]:
    result = []
    f = open(path)
    for line in f.read().splitlines():
        ins = line[0]
        val = int(line[1:])
        result.append((ins, val))
    return result


directions = {'E': (1, 0),
              'S': (0, -1),
              'W': (-1, 0),
              'N': (0, 1)}
number_to_direction = ['E', 'S', 'W', 'N']


class Ship:
    def __init__(self):
        self.position = (0, 0)
        self.direction = 0
        self.waypoint = (10, 1)

    def rotate(self, instruction: str, value: int) -> None:
        if instruction not in ['R', 'L']:
            return
        value //= 90
        if instruction == 'L':
            value = -value
        self.direction = (value + self.direction) % 4

    def step(self, instruction: str, value: int) -> None:
        if instruction in ['R', 'L']:
            self.rotate(instruction, value)
            return
        if instruction == 'F':
            instruction = number_to_direction[self.direction]
        dx, dy = directions[instruction]
        self.position = (self.position[0] + dx * value,
                         self.position[1] + dy * value)

    def rotate_waipoint(self, instruction: str, value: int) -> None:
        if instruction not in ['R', 'L']:
            return
        value %= 360
        if (instruction == 'R' and value == 90) or (instruction == 'L' and value == 270):
            self.waypoint = self.waypoint[1], -self.waypoint[0]
        elif(value == 180):
            self.waypoint = -self.waypoint[0], -self.waypoint[1]
        elif (instruction == 'L' and value == 90) or (instruction == 'R' and value == 270):
            self.waypoint = -self.waypoint[1], self.waypoint[0]

    def step_waipoint(self, instruction: str, value: int) -> None:
        if instruction == 'F':
            self.position = (self.position[0] + self.waypoint[0] * value,
                              self.position[1] + self.waypoint[1] * value)
        elif instruction in ['R', 'L']:
            self.rotate_waipoint(instruction, value)
        else:
            dx, dy = directions[instruction]
            self.waypoint = (self.waypoint[0] + dx * value,
                             self.waypoint[1] + dy * value)

    def move_ship(self, instructions: List[Tuple[str, int]], step_function: Callable[['Ship', str, int], None], debug: bool = False) -> None:
        for ins, val in instructions:
            step_function(self, ins, val)
            if debug:
                print(ins, val, ': ', self.position)

    def manhattan_distance(self) -> int:
        return abs(self.position[0]) + abs(self.position[1])


if __name__ == '__main__':
    print('Test01')
    test_ship = Ship()
    test_ship.move_ship([('F', 10), ('N', 3), ('F', 7),
                         ('R', 90), ('F', 11)], Ship.step, True)

    print('\nTask01')
    instructions = load_instructions('12/input.txt')
    ship = Ship()
    ship.move_ship(instructions, Ship.step)
    print('Manhattan distance: ', ship.manhattan_distance())

    print('Test02')
    test_ship = Ship()
    test_ship.move_ship([('F', 10), ('N', 3), ('F', 7),
                         ('R', 90), ('F', 11)], Ship.step_waipoint, True)

    print('\nTask02')
    instructions = load_instructions('12/input.txt')
    ship = Ship()
    ship.move_ship(instructions, Ship.step_waipoint)
    print('Manhattan distance: ', ship.manhattan_distance())
