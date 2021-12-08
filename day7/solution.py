from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass
class RawDigit:
    values: str
    _known_lengths = {
        1: 2,
        4: 4,
        7: 3,
        8: 7
    }

    def check_for(self, digit: int):
        return self._known_lengths.get(digit) == len(self.values)


@dataclass
class Reading:
    inputs: List[RawDigit]
    outputs: List[RawDigit]

with open('in.txt') as f:
    values = (line.strip() for line in f.readlines())
    splits = (line.split(' ') for line in values)

    readings: List[Reading] = []
    for line in splits:
        row_inputs = []
        row_outputs = []
        for i in range(10):
            row_inputs.append(RawDigit(line[i]))
        for i in range(11, 15):
            row_outputs.append(RawDigit(line[i]))
        readings.append(Reading(row_inputs, row_outputs))

count_first = 0
for r in readings:
    for o in r.outputs:
        if o.check_for(1) or o.check_for(4) or o.check_for(7) or o.check_for(8):
            count_first+=1

print(count_first)