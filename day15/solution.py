from typing import List


def parse_input() -> List[List[int]]:
    with open('in-p.txt') as f:
        values = [line.strip() for line in f.readlines()]
    cavern: List[List[int]] = []
    
    for i in range(2, len(values), 6):
        boards.append(Board.from_raw(values[i:i+5]))
    input_numbers = [int(num) for num in values[0].split(',')]
    return boards, input_numbers