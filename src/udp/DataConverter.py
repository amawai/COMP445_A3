from .Packet import Packet

MAX_PAYLOAD_SIZE = 1013

class DataConverter:
    @staticmethod
    def convert_data_to_packets(packet_type, peer_ip_addr, peer_port, data, max_seq_num):
        payloads = DataConverter.separate_payload(data)
        packets = []
        for seq_num, payload in enumerate(payloads):
            packet = Packet(packet_type=packet_type,
                   seq_num=seq_num % max_seq_num,
                   peer_ip_addr=peer_ip_addr,
                   peer_port=peer_port,
                   payload=payload.encode("utf-8"))
            packets.append(packet)
        return packets

    @staticmethod
    def separate_payload(payload):
        return [payload[i:min(len(payload) - 1, i+MAX_PAYLOAD_SIZE)] for i in range(0, len(payload.encode()), MAX_PAYLOAD_SIZE)] 