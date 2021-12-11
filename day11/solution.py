from typing import List, Tuple, Set


def parse_inputs() -> List[List[int]]:
    with open('in.txt') as f:
        return [list(map(int, list(line.strip()))) for line in f.readlines()]


def flash(row, col, state) -> Set[Tuple[int, int]]:
    ready_to_flash = set()
    for ver in range(-1, 2):
        for hor in range(-1, 2):
            next_row = row+ver
            next_col = col+hor
            if ver == 0 and hor == 0:
                continue
            if next_row < 0 or next_row >= len(state) or next_col < 0 or next_col >= len(state[row]):
                continue
            state[next_row][next_col] = state[next_row][next_col] + 1
            if state[next_row][next_col] > 9:
                ready_to_flash.add((next_row, next_col))
    return ready_to_flash


def reset_flashed(state):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] > 9:
                state[row][col] = 0


def do_step(state: List[List[int]]) -> int:
    to_flash = []
    flashed = set()
    for row in range(len(state)):
        for col in range(len(state[row])):
            state[row][col] = state[row][col] + 1
            if state[row][col] > 9:
                to_flash.append((row, col))
    while to_flash:
        octo_to_flash = to_flash.pop()
        if octo_to_flash not in flashed:
            ready_to_flash = flash(octo_to_flash[0], octo_to_flash[1], state)
            flashed.add(octo_to_flash)
            ready_to_flash = [octo for octo in ready_to_flash if octo not in flashed]
            to_flash.extend(ready_to_flash)
    reset_flashed(state)
    return len(flashed)


inputs = parse_inputs()
all_flashes = 0
for step in range(100):
    all_flashes += do_step(inputs)
print(all_flashes)

inputs = parse_inputs()
steps = 1
while do_step(inputs) < len(inputs) * len(inputs[0]):
    steps += 1
print(steps)
