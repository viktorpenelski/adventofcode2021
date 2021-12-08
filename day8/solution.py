from dataclasses import dataclass
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

    def intersection(self, raw: 'RawDigit'):
        return set.intersection(set(self.values), set(raw.values))

    def check_for(self, digit: int):
        return self._known_lengths.get(digit) == len(self.values)

    def __eq__(self, other):
        if not isinstance(other, RawDigit):
            return False
        return set(self.values) == set(other.values)


@dataclass
class Reading:
    inputs: List[RawDigit]
    outputs: List[RawDigit]

    def __init__(self, inputs: List[RawDigit], outputs: List[RawDigit]):
        self.inputs = inputs
        self.outputs = outputs
        self.known = self.parse_known(inputs)

    def digit_from_raw(self, raw: RawDigit):
        for digit, raw_digit in self.known.items():
            if raw_digit == raw:
                return digit
        raise Exception("we should know all digits :(")

    def output_digits(self) -> int:
        digits = 0
        for raw in self.outputs:
            digits = 10 * digits + self.digit_from_raw(raw)
        return digits



    @staticmethod
    def parse_known(inputs: List[RawDigit]):
        known = {}
        for i in inputs:
            vals = i.values
            if len(vals) == 2:
                known[1] = i
            elif len(vals) == 3:
                known[7] = i
            elif len(vals) == 4:
                known[4] = i
            elif len(vals) == 7:
                known[8] = i

        # we know 1, 4, 7 and 8

        for i in inputs:
            vals = i.values
            if len(vals) == 6 and len(i.intersection(known[1])) == 1:
                known[6] = i
            if len(vals) == 6 and len(i.intersection(known[4])) == 4:
                known[9] = i
        # we know 1, 4, 6, 7, 8, 9

        for i in inputs:
            vals = i.values
            if len(vals) == 6 and len(i.intersection(known[4])) == 3 and i != known[6]:
                known[0] = i
            if len(vals) == 5 and len(i.intersection(known[1])) == 2:
                known[3] = i

        # we know 0, 1, 3, 4, 6, 7, 8, 9

        for i in inputs:
            vals = i.values
            if len(vals) == 5 and len(i.intersection(known[6])) == 5:
                known[5] = i
            if len(vals) == 5 and len(i.intersection(known[6])) == 4 and i != known[3]:
                known[2] = i

        # we know all digits

        return known


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
    for raw_output in r.outputs:
        if raw_output.check_for(1) or raw_output.check_for(4) or raw_output.check_for(7) or raw_output.check_for(8):
            count_first+=1

print(count_first)

sum = 0
for r in readings:
    sum += r.output_digits()
print(sum)