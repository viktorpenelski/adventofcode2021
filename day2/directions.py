from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Reading:
    def __init__(self, horizontal=0, depth=0, aim=0):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

    def plus(self, reading: 'Reading') -> 'Reading':
        return Reading(self.horizontal + reading.horizontal,
                       self.depth + reading.depth,
                       self.aim + reading.aim)

    def multiplied(self) -> int:
        return self.horizontal * self.depth


class Direction(Protocol):
    @abstractmethod
    def move(self, reading: Reading) -> Reading:
        raise NotImplementedError


@dataclass
class Forward(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(horizontal=self.distance))


@dataclass
class Down(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(depth=self.distance))


@dataclass
class Up(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(depth=-self.distance))


@dataclass
class UpAim(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(aim=-self.distance))


@dataclass
class DownAim(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(aim=self.distance))


@dataclass
class ForwardAim(Direction):
    distance: int

    def move(self, reading: Reading) -> Reading:
        return reading.plus(Reading(horizontal=self.distance, depth=self.distance * reading.aim))

