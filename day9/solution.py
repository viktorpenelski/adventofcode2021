from queue import PriorityQueue
from typing import List, Set, Tuple


def lower_than_neighbours(row: int, col: int, heatmap: List[List[int]]) -> bool:
    for ver in range(-1, 2):
        for hor in range(-1, 2):
            if ver == 0 and hor == 0:
                continue
            if ver != 0 and hor != 0:
                continue
            if row+ver < 0 or row+ver >= len(heatmap):
                continue
            if col+hor < 0 or col+hor >= len(heatmap[row]):
                continue
            if heatmap[row][col] >= heatmap[row + ver][col + hor]:
                return False
    return True


def basin_size_around(row: int, col: int, heatmap: List[List[int]], visited: Set[Tuple[int, int]]):
    if (row, col) in visited:
        return 0
    if row < 0 or col < 0:
        return 0
    if row >= len(heatmap) or col >= len(heatmap[row]):
        return 0
    if heatmap[row][col] == 9:
        return 0
    visited.add((row, col))
    up = basin_size_around(row + 1, col, heatmap, visited)
    down = basin_size_around(row - 1, col, heatmap, visited)
    left = basin_size_around(row, col - 1, heatmap, visited)
    right = basin_size_around(row, col + 1, heatmap, visited)
    return 1 + up + down + left + right


inputs: List[List[int]]
with open('in.txt') as f:
    inputs = [list(map(int, list(x.strip()))) for x in f.readlines()]

risk_level_sum = 0
q = PriorityQueue()
for row in range(len(inputs)):
    for col in range(len(inputs[row])):
        if lower_than_neighbours(row, col, inputs):
            basin = basin_size_around(row, col, inputs, set())
            q.put((-basin, (row, col)))
            risk_level_sum += inputs[row][col] + 1
print(risk_level_sum)

print(abs(q.get()[0] * q.get()[0] * q.get()[0]))
