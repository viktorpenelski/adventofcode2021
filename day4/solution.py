from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Dict, Set


@dataclass
class Position:
    row: int
    col: int


class Board:
    numbers: List[List[int]]
    lookup: Dict[int, List[Position]]
    _number_hits: Set[int]
    _row_hits: Dict[int, int]
    _col_hits: Dict[int, int]
    won: bool = False

    def __init__(self, numbers: List[List[int]]):
        self.numbers = numbers
        self.lookup = defaultdict(lambda: [])
        self._number_hits = set()
        self._row_hits = defaultdict(lambda: 0)
        self._col_hits = defaultdict(lambda: 0)
        for row, line in enumerate(numbers):
            for col, num in enumerate(line):
                self.lookup[num].append(Position(row, col))

    @staticmethod
    def from_raw(lines: List[str]) -> 'Board':
        nums = [[int(num) for num in line.split()] for line in lines]
        assert 5 == len(nums), "board must have 5 rows!"
        for line in nums:
            assert 5 == len(line), f"row {line} must have 5 numbers!"
        return Board(numbers=nums)

    def visit(self, num: int) -> bool:
        positions = self.lookup[num]
        if len(positions) > 0:
            self._number_hits.add(num)
            for pos in positions:
                self._row_hits[pos.row] = self._row_hits[pos.row] + 1
                self._col_hits[pos.col] = self._col_hits[pos.col] + 1
                if 5 == self._row_hits[pos.row] or 5 == self._col_hits[pos.col]:
                    self.won = True
                    return True
        return False

    def sum_not_hit_numbers(self) -> int:
        return reduce(lambda so_far, num: so_far if num in self._number_hits else so_far + num,
                      [num for row in self.numbers for num in row],
                      0)


def parse_input(filename: str) -> (List[Board], List[int]):
    with open(filename) as f:
        values = [line.strip() for line in f.readlines()]
    boards: List[Board] = []
    for i in range(2, len(values), 6):
        boards.append(Board.from_raw(values[i:i+5]))
    input_numbers = [int(num) for num in values[0].split(',')]
    return boards, input_numbers


def solve() -> None:
    boards, input_numbers = parse_input('in-p.txt')
    boards_won = 0
    for num in input_numbers:
        for board in boards:
            if not board.won:
                bingo = board.visit(num)
                if bingo:
                    boards_won += 1
                    if boards_won == 1 or boards_won == len(boards):
                        print(board.numbers)
                        print(f'sum of unvisited numbers: {board.sum_not_hit_numbers()}')
                        print(f'winning number: {num}')
                        print(f'score: {board.sum_not_hit_numbers() * num}')


solve()
