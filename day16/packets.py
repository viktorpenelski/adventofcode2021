from abc import abstractmethod, ABC
from functools import reduce
from typing import Tuple, List


def _get_packet_version(binary_string: str):
    return int(binary_string[3:6], 2)


def packet_factory(binary_string: str):
    if _get_packet_version(binary_string) == 4:
        return LiteralPacket(binary_string)
    else:
        return OpPacket.instantiate(binary_string)


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
    def __init__(self, binary_string: str):
        super().__init__(binary_string)
        self.type_length_id = int(self.binary_string[6], 2)
        packets, last_pos = self.get_packets_and_len(binary_string)
        self.packets = packets
        self.last_pos = last_pos

    def sum_versions(self):
        return self.version + sum([p.sum_versions() for p in self.packets])

    def value(self) -> int:
        values = [v.value() for v in self.packets]
        if self.id == 0:
            return sum(values)
        if self.id == 1:
            return reduce(lambda a, b: a*b, values, 1)
        if self.id == 2:
            return min(values)
        if self.id == 3:
            return max(values)
        if self.id == 5:
            return int(values[0] > values[1])
        if self.id == 6:
            return int(values[0] < values[1])
        if self.id == 7:
            return int(values[0] == values[1])

    @staticmethod
    def instantiate(binary_string: str) -> 'OpPacket':
        type_length_id = int(binary_string[6], 2)
        if type_length_id == 0:
            return BitsLenOpPacket(binary_string)
        else:
            return NumLenOpPacket(binary_string)

    @abstractmethod
    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        pass

    def _get_last_bit_pos(self) -> int:
        return self.last_pos


class BitsLenOpPacket(OpPacket):
    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 15 bits are total length in bits of sub-packets
        sub_packet_length = int(binary_string[7:22], 2)
        last_bit_pos = 22 + sub_packet_length
        sub_packet_bits = binary_string[22:last_bit_pos]
        packets = []
        while len(sub_packet_bits) > 0:
            p = packet_factory(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p._get_last_bit_pos():]
            packets.append(p)

        return packets, last_bit_pos


class NumLenOpPacket(OpPacket):

    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 11 bits are the number of sub-packets immediately contained by this packet
        nr_sub_packets = int(binary_string[7:18], 2)
        sub_packet_bits = binary_string[18:]
        packets = []
        while nr_sub_packets > 0:
            p = packet_factory(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p._get_last_bit_pos():]
            packets.append(p)
            nr_sub_packets -= 1
        return packets, len(binary_string) - len(sub_packet_bits)
