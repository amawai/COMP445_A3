from .Packet import Packet
from .PacketTypes import PacketTypes

packet_types = PacketTypes()

MAX_SEQUENCE_NUMBER = 10
class RecWindow:
    def __init__(self, max_seq_num=MAX_SEQUENCE_NUMBER):
        self.buffer = []
        self.max_seq_num = max_seq_num
        self.current_seq_start = 0
        self.window_size = int(self.max_seq_num / 2)
        self.window = dict.fromkeys([seq for seq in range(0, self.max_seq_num)])
        self.buffer_ready = False
    
    def buffer_ready_for_extraction(self):
        return self.buffer_ready

    def extract_buffer(self):
        return "".join(self.buffer)

    def get_current_window(self):
        return [window[index] for index in self.valid_sequence_nums()]

    #Returns tuple of (packet_type, seq_num)
    def insert_packet(self, packet):
        print('trying to insert packet ', packet.seq_num)
        if packet.seq_num in self.valid_sequence_nums():
            self.window[packet.seq_num] = packet
            #check if the packet is a final packet type
            if packet.packet_type == packet_types.FINAL_PACKET:
                self.final_flag = True
        return self.check_window_for_ack_or_nak()

    def check_window_for_ack_or_nak(self):
        window_has_slid = False
        for index in self.valid_sequence_nums():
            current_packet = self.window[index]
            if index == self.current_seq_start and current_packet != None:
                print('current sequence number is ', self.current_seq_start)
                #We know that this packet is complete, add it to the buffer
                self.buffer.append(current_packet.payload.decode('utf-8'))
                self.slide()
                window_has_slid = True
                if (current_packet.packet_type == packet_types.FINAL_PACKET):
                    print("all packets have been received")
                    self.buffer_ready = True
        if (window_has_slid):
            #Send an ACK denoting the last successful frame
            return (packet_types.ACK, (self.current_seq_start - 1)% self.max_seq_num)
        else:
            #Send NAk indicating that this current frame is missing
            return (packet_types.NAK, self.current_seq_start)

    def slide(self):
        #Reset the window so that it can receive a new packet
        self.window[self.current_seq_start] = None
        self.current_seq_start = (self.current_seq_start + 1) % self.max_seq_num
        print('sliding! new seq: ', self.current_seq_start)
    
    def valid_sequence_nums(self):
        return [num % self.max_seq_num for num in range(self.current_seq_start, self.current_seq_start + self.window_size)]