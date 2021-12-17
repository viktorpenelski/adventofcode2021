from abc import abstractmethod, ABC
from typing import Tuple, List, Callable


class Packet(ABC):
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.version = int(binary_string[0:3], 2)
        self.id = int(binary_string[3:6], 2)

    @abstractmethod
    def _get_last_bit_pos(self):
        pass

    @abstractmethod
    def sum_versions(self):
        pass

    @abstractmethod
    def value(self) -> int:
        pass


class UnpackStrategy(ABC):

    def __init__(self, packet_factory: Callable[[str], Packet]):
        self.packet_factory = packet_factory

    @abstractmethod
    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        pass


class LiteralPacket(Packet):

    def __init__(self, binary_string: str):
        super().__init__(binary_string)
        literal, pos = self._calculate_literal(binary_string)
        self.literal = literal
        self.last_pos = pos

    def _get_last_bit_pos(self):
        return self.last_pos

    def sum_versions(self):
        return self.version

    def value(self) -> int:
        return self.literal

    @staticmethod
    def _calculate_literal(binary_string: str) -> Tuple[int, int]:
        bit_pos = 6
        extracted_num = ""
        while binary_string[bit_pos] == "1":
            extracted_num += binary_string[bit_pos+1:bit_pos+5]
            bit_pos += 5
        last_post = bit_pos + 5
        extracted_num += binary_string[bit_pos+1:last_post]
        return int(extracted_num, 2), last_post


class OpPacket(Packet, ABC):
    """All inheriting members should include an ADVERTISE_ID int field."""

    def __init__(self, binary_string: str, strategy: UnpackStrategy):
        super().__init__(binary_string)
        self.type_length_id = int(self.binary_string[6], 2)
        packets, last_pos = strategy.get_packets_and_len(binary_string)
        self.packets = packets
        self.last_pos = last_pos

    def sum_versions(self):
        return self.version + sum([p.sum_versions() for p in self.packets])

    def value(self) -> int:
        values = [v.value() for v in self.packets]
        return self._calculate_value(values)

    @abstractmethod
    def _calculate_value(self, values: List[int]):
        pass

    def _get_last_bit_pos(self) -> int:
        return self.last_pos

