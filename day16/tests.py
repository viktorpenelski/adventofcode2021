import unittest

from day16.solution import Packet, hex_to_bin
from day16.packets import BitsLenOpPacket, NumLenOpPacket, OpPacket, LiteralPacket, packet_factory


class Tests(unittest.TestCase):

    def test_compare_more_true(self):
        # 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
        packet = packet_factory(hex_to_bin("9C0141080250320F1802104A08"))
        self.assertEqual(1, packet.value())

    def test_compare_more_false(self):
        # 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
        packet = packet_factory(hex_to_bin("9C005AC2F8F0"))
        self.assertEqual(0, packet.value())

    def test_compare_less_false(self):
        # F600BC2D8F produces 0, because 5 is not greater than 15.
        packet = packet_factory(hex_to_bin("F600BC2D8F"))
        self.assertEqual(0, packet.value())

    def test_compare_less_true(self):
        # D8005AC2A8F0 produces 1, because 5 is less than 15.
        packet = packet_factory(hex_to_bin("D8005AC2A8F0"))
        self.assertEqual(1, packet.value())

    def test_find_max(self):
        # CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
        packet = packet_factory(hex_to_bin("CE00C43D881120"))
        self.assertEqual(9, packet.value())

    def test_find_min(self):
        # 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
        packet = packet_factory(hex_to_bin("880086C3E88112"))
        self.assertEqual(7, packet.value())

    def test_prod(self):
        # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
        packet = packet_factory(hex_to_bin("04005AC33890"))
        self.assertEqual(54, packet.value())

    def test_sum(self):
        # C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
        packet = packet_factory(hex_to_bin("C200B40A82"))
        self.assertEqual(3, packet.value())

    def test_tripple_nested_op_with_five_packets(self):
        packet = packet_factory(hex_to_bin("A0016C880162017C3686B18A3D4780"))
        assert BitsLenOpPacket == type(packet)
        self.assertEqual(31, packet.sum_versions())

    def test_multi_bits_len_nested_op(self):
        packet = packet_factory(hex_to_bin("C0015000016115A2E0802F182340"))
        assert BitsLenOpPacket == type(packet)
        self.assertEqual(23, packet.sum_versions())

    def test_multi_num_len_nested_op(self):
        packet = packet_factory(hex_to_bin("620080001611562C8802118E34"))
        assert NumLenOpPacket == type(packet)
        self.assertEqual(12, packet.sum_versions())

    def test_num_len_nested_op(self):
        packet = packet_factory(hex_to_bin("8A004A801A8002F478"))
        assert NumLenOpPacket == type(packet)
        self.assertEqual(16, packet.sum_versions())

    def test_operator_packet_1(self):
        packet = packet_factory(hex_to_bin("EE00D40C823060"))
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
        self.assertEqual(51, packet._get_last_bit_pos())

    def test_operator_packet_0(self):
        packet = packet_factory(hex_to_bin("38006F45291200"))
        self.assertEqual(1, packet.version)
        self.assertEqual(6, packet.id)
        self.assertEqual(0, packet.type_length_id)
        self.assertEqual(2, len(packet.packets))
        self.assertEqual(LiteralPacket, type(packet.packets[0]))
        self.assertEqual(LiteralPacket, type(packet.packets[1]))
        self.assertEqual(10, packet.packets[0].literal)
        self.assertEqual(20, packet.packets[1].literal)
        self.assertEqual(49, packet._get_last_bit_pos())

    def test_literal_packet(self):
        packet = LiteralPacket("110100101111111000101000")
        self.assertEqual(2021, packet.literal)

    def test_hex_to_bin(self):
        self.assertEqual(hex_to_bin("D2FE28"), "110100101111111000101000")
        self.assertEqual(hex_to_bin("38006F45291200"), "00111000000000000110111101000101001010010001001000000000")
        self.assertEqual(hex_to_bin("EE00D40C823060"), "11101110000000001101010000001100100000100011000001100000")
