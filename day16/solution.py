from day16.packets import Packet, packet_factory


def parse_input() -> str:
    with open("in.txt") as f:
        return hex_to_bin(f.readline())


def hex_to_bin(hex_str: str) -> str:
    out = ""
    for c in hex_str:
        int_line = int(c, 16)
        out += format(int_line, "04b")
    return out



if __name__ == '__main__':
    packet = packet_factory(parse_input())
    print(packet.sum_versions())
    print(packet.value())
