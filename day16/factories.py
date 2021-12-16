def _get_all_op_subclasses():
    from day16.packets import OpPacket

    import day16.op_packets
    subclass_list = []

    def recurse(klass):
        for subclass in klass.__subclasses__():
            subclass_list.append(subclass)
            recurse(subclass)

    recurse(OpPacket)

    return {clazz.ADVERTISE_ID: clazz for clazz in subclass_list}


def packet_factory(binary_string: str) -> 'Packet':
    from day16.packets import LiteralPacket
    from day16.unpack_strategies import NumLenUnpackStrategy, BitsLenUnpackStrategy

    packet_id = int(binary_string[3:6], 2)

    if packet_id == 4:
        return LiteralPacket(binary_string)
    else:
        type_length_id = int(binary_string[6], 2)
        strategy = BitsLenUnpackStrategy(packet_factory) if type_length_id == 0 else NumLenUnpackStrategy(packet_factory)
        return _get_all_op_subclasses()[packet_id](binary_string, strategy)

