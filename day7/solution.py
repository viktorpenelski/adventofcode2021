from functools import reduce
from typing import List, Callable


def min_fuel(reduce_fun: Callable, positions: List[int]) -> int:
    return min([reduce(reduce_fun(i), positions, 0) for i in range(max(positions))])


with open('in.txt') as f:
    _line = f.readline()
    positions = list(map(int, _line.split(',')))
cost_first = lambda idx: lambda acc, pos: acc + abs(pos - idx)
cost_second = lambda idx: lambda acc, pos: acc + (abs(pos - idx) * (1 + abs(pos - idx)) / 2)
print(min_fuel(cost_first, positions))
print(min_fuel(cost_second, positions))
