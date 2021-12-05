from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def one_step_to(self, pt: 'Point') -> 'Point':
        def _direction(first: int, second: int) -> int:
            if first == second:
                return 0
            elif first - second > 0:
                return -1  # decrement current to move a step towards target
            else:
                return 1  # when first-second < 0, need to increment first to move towards target

        return Point(
            self.x + _direction(self.x, pt.x),
            self.y + _direction(self.y, pt.y)
        ) 


@dataclass(frozen=True)
class Line:
    first_point: Point
    second_point: Point


def parse_inputs() -> List[Line]:
    input_lines = []
    with open('in.txt') as f:
        values = (line.strip() for line in f.readlines())   #  0,9 -> 5,9
        split = (line.split(' -> ') for line in values)     # ['0,9', '5,9']
    for line in split:
        first = line[0].split(',')                          # ['0', '9']
        second = line[1].split(',')                         # ['5', '9']
        p1 = Point(int(first[0]), int(first[1]))
        p2 = Point(int(second[0]), int(second[1]))
        input_lines.append(Line(p1, p2))
    return input_lines


def solve(consider_diagonals: bool = True) -> int:
    ocean_floor: Dict[Point, int] = {}
    lines = parse_inputs()

    for line in lines:
        if not consider_diagonals and not(line.first_point.x == line.second_point.x or line.first_point.y == line.second_point.y):
            continue
        pos = line.first_point
        while (pos != line.second_point):
            ocean_floor[pos] = ocean_floor.get(pos, 0) + 1
            pos = pos.one_step_to(line.second_point)
        ocean_floor[pos] = ocean_floor.get(pos, 0) + 1  # don't forget to add 2nd point
    
    intersections = [n for n in ocean_floor.values() if n > 1]
    return len(intersections)

print(solve(False))
print(solve())
