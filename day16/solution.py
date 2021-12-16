from abc import abstractmethod, ABC
import unittest
from functools import reduce
from typing import Tuple, List


def parse_input() -> str:
    with open("in.txt") as f:
        return hex_to_bin(f.readline())


def hex_to_bin(hex_str: str) -> str:
    out = ""
    for c in hex_str:
        int_line = int(c, 16)
        out += format(int_line, "04b")
    return out


class Packet(ABC):
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.version = int(binary_string[0:3], 2)
        self.id = int(binary_string[3:6], 2)

    @abstractmethod
    def get_last_bit_pos(self):
        pass

    @abstractmethod
    def sum_versions(self):
        pass

    @staticmethod
    def instantiate(binary_str: str) -> 'Packet':
        if int(binary_str[3:6], 2) == 4:
            return LiteralPacket(binary_str)
        else:
            return OpPacket.instantiate(binary_str)

    @abstractmethod
    def value(self) -> int:
        pass


class LiteralPacket(Packet):

    def __init__(self, binary_string: str):
        super().__init__(binary_string)
        literal, pos = self._calculate_literal(binary_string)
        self.literal = literal
        self.last_pos = pos

    def get_last_bit_pos(self):
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
        if self.id == 0:
            return sum([v.value() for v in self.packets])
        if self.id == 1:
            return reduce(lambda a, b: a*b, [v.value() for v in self.packets], 1)
        if self.id == 2:
            min_p = None
            for p in self.packets:
                if min_p is None or min_p.value() > p.value():
                    min_p = p
            return min_p.value()
        if self.id == 3:
            max_p = None
            for p in self.packets:
                if max_p is None or max_p.value() < p.value():
                    max_p = p
            return max_p.value()
        if self.id == 5:
            if self.packets[0].value() > self.packets[1].value():
                return 1
            else:
                return 0
        if self.id == 6:
            if self.packets[0].value() < self.packets[1].value():
                return 1
            else:
                return 0
        if self.id == 7:
            if self.packets[0].value() == self.packets[1].value():
                return 1
            else:
                return 0

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

    def get_last_bit_pos(self) -> int:
        return self.last_pos


class BitsLenOpPacket(OpPacket):
    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 15 bits are total length in bits of sub-packets
        sub_packet_length = int(binary_string[7:22], 2)
        last_bit_pos = 22 + sub_packet_length
        sub_packet_bits = binary_string[22:last_bit_pos]
        packets = []
        while len(sub_packet_bits) > 0:
            p = Packet.instantiate(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p.get_last_bit_pos():]
            packets.append(p)

        return packets, last_bit_pos


class NumLenOpPacket(OpPacket):

    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 11 bits are the number of sub-packets immediately contained by this packet
        nr_sub_packets = int(binary_string[7:18], 2)
        sub_packet_bits = binary_string[18:]
        packets = []
        while nr_sub_packets > 0:
            p = Packet.instantiate(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p.get_last_bit_pos():]
            packets.append(p)
            nr_sub_packets -= 1
        return packets, len(binary_string) - len(sub_packet_bits)





class Tests(unittest.TestCase):

    def test_compare_more_true(self):
        # 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
        packet = Packet.instantiate(hex_to_bin("9C0141080250320F1802104A08"))
        self.assertEqual(1, packet.value())

    def test_compare_more_false(self):
        # 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
        packet = Packet.instantiate(hex_to_bin("9C005AC2F8F0"))
        self.assertEqual(0, packet.value())

    def test_compare_less_false(self):
        # F600BC2D8F produces 0, because 5 is not greater than 15.
        packet = Packet.instantiate(hex_to_bin("F600BC2D8F"))
        self.assertEqual(0, packet.value())

    def test_compare_less_true(self):
        # D8005AC2A8F0 produces 1, because 5 is less than 15.
        packet = Packet.instantiate(hex_to_bin("D8005AC2A8F0"))
        self.assertEqual(1, packet.value())

    def test_find_max(self):
        # CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
        packet = Packet.instantiate(hex_to_bin("CE00C43D881120"))
        self.assertEqual(9, packet.value())

    def test_find_min(self):
        # 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
        packet = Packet.instantiate(hex_to_bin("880086C3E88112"))
        self.assertEqual(7, packet.value())

    def test_prod(self):
        # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
        packet = Packet.instantiate(hex_to_bin("04005AC33890"))
        self.assertEqual(54, packet.value())

    def test_sum(self):
        # C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
        packet = Packet.instantiate(hex_to_bin("C200B40A82"))
        self.assertEqual(3, packet.value())

    def test_tripple_nested_op_with_five_packets(self):
        packet = Packet.instantiate(hex_to_bin("A0016C880162017C3686B18A3D4780"))
        assert BitsLenOpPacket == type(packet)
        self.assertEqual(31, packet.sum_versions())

    def test_multi_bits_len_nested_op(self):
        packet = Packet.instantiate(hex_to_bin("C0015000016115A2E0802F182340"))
        assert BitsLenOpPacket == type(packet)
        self.assertEqual(23, packet.sum_versions())

    def test_multi_num_len_nested_op(self):
        packet = Packet.instantiate(hex_to_bin("620080001611562C8802118E34"))
        assert NumLenOpPacket == type(packet)
        self.assertEqual(12, packet.sum_versions())

    def test_num_len_nested_op(self):
        packet = Packet.instantiate(hex_to_bin("8A004A801A8002F478"))
        assert NumLenOpPacket == type(packet)
        self.assertEqual(16, packet.sum_versions())

    def test_operator_packet_1(self):
        packet = OpPacket.instantiate(hex_to_bin("EE00D40C823060"))
        self.assertEqual(7, packet.version)
        self.assertEqual(3, packet.id)
        self.assertEqual(1, packet.type_length_id)
        self.assertEqual(3, len(packet.packets))
        self.assertEqual(LiteralPacket, type(packet.packets[0]))
        self.assertEqual(LiteralPacket, type(packet.packets[1]))
        self.assertEqual(LiteralPacket, type(packet.packets[2]))
        self.assertEqual(1, packet.packets[0].literal)
        self.assertEqual(2, packet.packets[1].literal)
        self.assertEqual(3, packet.packets[2].literal)
        self.assertEqual(51, packet.get_last_bit_pos())

    def test_operator_packet_0(self):
        packet = OpPacket.instantiate(hex_to_bin("38006F45291200"))
        self.assertEqual(1, packet.version)
        self.assertEqual(6, packet.id)
        self.assertEqual(0, packet.type_length_id)
        self.assertEqual(2, len(packet.packets))
        self.assertEqual(LiteralPacket, type(packet.packets[0]))
        self.assertEqual(LiteralPacket, type(packet.packets[1]))
        self.assertEqual(10, packet.packets[0].literal)
        self.assertEqual(20, packet.packets[1].literal)
        self.assertEqual(49, packet.get_last_bit_pos())


    def test_literal_packet(self):
        packet = LiteralPacket("110100101111111000101000")
        self.assertEqual(2021, packet.literal)

    def test_hex_to_bin(self):
        self.assertEqual(hex_to_bin("D2FE28"), "110100101111111000101000")
        self.assertEqual(hex_to_bin("38006F45291200"), "00111000000000000110111101000101001010010001001000000000")
        self.assertEqual(hex_to_bin("EE00D40C823060"), "11101110000000001101010000001100100000100011000001100000")


if __name__ == '__main__':
    unittest.main()
    # packet = Packet.instantiate(parse_input())
    # print(packet.sum_versions())
    # print(packet.value())
