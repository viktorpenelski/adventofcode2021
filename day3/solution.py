from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Set, List


@dataclass
class BitCount:
    ones: int = 0
    zeroes: int = 0

    def add(self, bc: 'BitCount') -> 'BitCount':
        return BitCount(self.ones + bc.ones, self.zeroes + bc.zeroes)

    def most_common(self) -> str:
        return '1' if self.ones >= self.zeroes else '0'

    def least_common(self) -> str:
        return '0' if self.zeroes <= self.ones else '1'


def map_bit_counts(inputs: List[str]) -> Dict[int, BitCount]:
    mapped_bit_counts: Dict[int, BitCount] = defaultdict(lambda: BitCount())
    for value in inputs:
        for i, ch in enumerate(value):
            bc = BitCount(ones=1) if ch == '1' else BitCount(zeroes=1)
            mapped_bit_counts[i] = mapped_bit_counts[i].add(bc)
    return mapped_bit_counts


def filter_inputs(inputs: List[str], target: str = 'most') -> str:
    bit_position = 0
    inputs = inputs.copy()
    while len(inputs) > 1:
        mapped_bit_counts = map_bit_counts(inputs)
        if 'most' == target:
            target_bit = mapped_bit_counts[bit_position].most_common()
        else:
            target_bit = mapped_bit_counts[bit_position].least_common()
        inputs = [inp for inp in inputs if inp[bit_position] == target_bit]
        bit_position += 1
    return inputs[0]


with open('in.txt') as f:
    values = [line.strip() for line in f.readlines()]

bit_counts = map_bit_counts(values)

gamma = ''
epsilon = ''
for i in range(len(values[0])):
    gamma += bit_counts[i].most_common()
    epsilon += bit_counts[i].least_common()

print(int(gamma, 2) * int(epsilon, 2))
oxygen = filter_inputs(values)
co2 = filter_inputs(values, 'least')
print(int(oxygen, 2) * int(co2, 2))
