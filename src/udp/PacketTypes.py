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