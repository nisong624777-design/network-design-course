import struct

class Packet:
    # Header Format: ! (Network Byte Order), B (Type, 1B), I (Seq, 4B), H (Len, 2B)
    # Total header size = 7 bytes
    HEADER_FORMAT = "!BIH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, pkt_type, seq_num, data=b""):
        self.pkt_type = pkt_type  # 0: Data/Echo, 1: EOF
        self.seq_num = seq_num
        self.data = data
        self.data_len = len(data)

    def encode(self):
        
        header = struct.pack(self.HEADER_FORMAT, self.pkt_type, self.seq_num, self.data_len)
        return header + self.data

    @staticmethod
    def decode(raw_bytes):
        
        header_bytes = raw_bytes[:Packet.HEADER_SIZE]
        payload = raw_bytes[Packet.HEADER_SIZE:]
        pkt_type, seq_num, data_len = struct.unpack(Packet.HEADER_FORMAT, header_bytes)
        return Packet(pkt_type, seq_num, payload[:data_len])