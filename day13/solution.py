from dataclasses import dataclass
from typing import Tuple, List
import copy


def parse_input():
    def parse_coord(line: str) -> Tuple[int, int]:
        x, y = map(int, line.split(','))
        return x, y

    def parse_fold(line: str) -> Tuple[int, int]:
        split = line.split('=')
        if line.startswith('fold along y'):
            return 0, int(split[1])
        if line.startswith('fold along x'):
            return int(split[1]), 0
        raise Exception(f'Fold should always start with fold along x or y, but was: {line}')

    dots = []
    folds = []
    max_row = 0
    max_col = 0
    with open('in.txt') as f:
        for l in f.readlines():
            stripped = l.strip()
            if len(stripped) == 0:
                continue
            if not stripped.startswith('fold'):
                x, y = parse_coord(stripped)
                dots.append((x, y))
                if x > max_col:
                    max_col = x
                if y > max_row:
                    max_row = y
            else:
                folds.append(parse_fold(stripped))

    return Paper.from_dots(dots, max_row + 1, max_col + 1), folds


@dataclass
class Paper:
    state: List[List[bool]]

    @staticmethod
    def from_dots(dots: List[Tuple[int, int]], rows, cols):
        state = [[False] * cols for i in range(rows)]
        for dot in dots:
            state[dot[1]][dot[0]] = True
        return Paper(state)

    def count_dots(self):
        return sum(x.count(True) for x in self.state)

    def print(self):
        for r in range(len(self.state)):
            row = ''
            for c in range(len(self.state[r])):
                if self.state[r][c]:
                    row += '█'
                else:
                    row += ' '
            print(row)

    def fold(self, row: int, col: int):
        state = copy.deepcopy(self.state)
        if row != 0:
            distance = 1
            while row + distance < len(state) and row-distance >= 0:
                for c in range(len(state[row + distance])):
                    state[row - distance][c] = state[row - distance][c] or state[row + distance][c]
                distance += 1
            return Paper(state[0:row])
        if col != 0:
            for row in range(len(state)):
                state[row] = state[row][0:col]
            distance = 1
            while col + distance < len(self.state[0]) and col - distance >= 0:
                for r in range(len(state)):
                    state[r][col - distance] = self.state[r][col-distance] or self.state[r][col+distance]
                distance += 1
            return Paper(state)


paper, folds = parse_input()
fold = paper
for x, y in folds:
    fold = fold.fold(y, x)
    fold.print()
    print(fold.count_dots())
    print(chr(fold.count_dots()))
