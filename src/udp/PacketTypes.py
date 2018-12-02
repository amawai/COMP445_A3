class PacketTypes:
    @property
    def DATA(self):
        return 0
    
    @property
    def ACK(self):
        return 1
    
    @property
    def NAK(self):
        return 2
    
    @property
    def SYN(self):
        return 3
    
    @property
    def SYN_ACK(self):
        return 4

    @property
    def FINAL_REC_PACKET(self):
        return 5
    
    @property
    def FINAL_SEND_PACKET(self):
        return 6

    @staticmethod
    def get_packet_name(packet_type):
        if packet_type == 0:
            return "DATA"
        elif packet_type == 1:
            return "ACK"
        elif packet_type == 2:
            return "NAK"
        elif packet_type == 3:
            return "SYN"
        elif packet_type == 4:
            return "SYN_ACK"
        elif packet_type == 5:
            return "FINAL_REC_PACKET"
        elif packet_type == 6:
            return "FINAL_SEND_PACKET"
        else:
            return "UNKNOWN LOL"