from typing import Tuple, List

from day16.packets import Packet, UnpackStrategy


class BitsLenUnpackStrategy(UnpackStrategy):

    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 15 bits are total length in bits of sub-packets
        sub_packet_length = int(binary_string[7:22], 2)
        last_bit_pos = 22 + sub_packet_length
        sub_packet_bits = binary_string[22:last_bit_pos]
        packets = []
        while len(sub_packet_bits) > 0:
            p = self.packet_factory(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p._get_last_bit_pos():]
            packets.append(p)

        return packets, last_bit_pos


class NumLenUnpackStrategy(UnpackStrategy):

    def get_packets_and_len(self, binary_string: str) -> Tuple[List[Packet], int]:
        # next 11 bits are the number of sub-packets immediately contained by this packet
        nr_sub_packets = int(binary_string[7:18], 2)
        sub_packet_bits = binary_string[18:]
        packets = []
        while nr_sub_packets > 0:
            p = self.packet_factory(sub_packet_bits)
            sub_packet_bits = sub_packet_bits[p._get_last_bit_pos():]
            packets.append(p)
            nr_sub_packets -= 1
        return packets, len(binary_string) - len(sub_packet_bits)
