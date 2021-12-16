from functools import reduce
from typing import List

from day16.packets import OpPacket


class OpSumPacket(OpPacket):
    ADVERTISE_ID = 0

    def _calculate_value(self, values: List[int]) -> int:
        return sum(values)


class OpMulPacket(OpPacket):
    ADVERTISE_ID = 1

    def _calculate_value(self, values: List[int]):
        return reduce(lambda a, b: a * b, values, 1)


class OpMinPacket(OpPacket):
    ADVERTISE_ID = 2

    def _calculate_value(self, values: List[int]):
        return min(values)


class OpMaxPacket(OpPacket):
    ADVERTISE_ID = 3

    def _calculate_value(self, values: List[int]):
        return max(values)


class OpGtPacket(OpPacket):
    ADVERTISE_ID = 5

    def _calculate_value(self, values: List[int]):
        return int(values[0] > values[1])


class OpLtPacket(OpPacket):
    ADVERTISE_ID = 6

    def _calculate_value(self, values: List[int]):
        return int(values[0] < values[1])


class OpEqPacket(OpPacket):
    ADVERTISE_ID = 7

    def _calculate_value(self, values: List[int]):
        return int(values[0] == values[1])
