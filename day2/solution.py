from functools import reduce
from typing import Sequence

from day2.directions import Reading
from day2.factories import DirectionsFactory, DirectionsFactoryAim, Factory


def calculate(factory: Factory, lines: Sequence[str]) -> int:
    directions = [factory.parse_line(line) for line in lines]
    last_reading = reduce(lambda latest_reading, direction: direction.move(latest_reading),
                          directions,
                          Reading())
    return last_reading.multiplied()


with open('in.txt') as f:
    values = [line.strip() for line in f.readlines()]

print(calculate(DirectionsFactory(), values))
print(calculate(DirectionsFactoryAim(), values))
