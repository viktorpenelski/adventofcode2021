from asyncio import Protocol

from day2.directions import UpAim, DownAim, Forward, Up, Down, Direction, ForwardAim


class Factory(Protocol):
    @staticmethod
    def parse_line(line: str) -> Direction:
        raise NotImplementedError


class DirectionsFactory(Factory):

    @staticmethod
    def parse_line(line: str) -> Direction:
        direction, distance = line.split()
        distance = int(distance)
        if 'forward' == direction:
            return Forward(distance)
        elif 'up' == direction:
            return Up(distance)
        elif 'down' == direction:
            return Down(distance)
        else:
            raise ValueError(line)


class DirectionsFactoryAim(Factory):

    @staticmethod
    def parse_line(line: str) -> Direction:
        direction, distance = line.split()
        distance = int(distance)
        if 'forward' == direction:
            return ForwardAim(distance)
        elif 'up' == direction:
            return UpAim(distance)
        elif 'down' == direction:
            return DownAim(distance)
        else:
            raise ValueError(line)