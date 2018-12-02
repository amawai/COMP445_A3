from Packet import Packet
from PacketTypes import PacketTypes

packet_types = PacketTypes()

class RecWindow:
    def __init__(self, max_seq_num):
        self.buffer = []
        self.max_seq_num = max_seq_num
        self.current_seq_start = 0
        self.window_size = int(self.max_seq_num / 2)
        self.window = dict.fromkeys([seq for seq in range(0, self.max_seq_num)])
        self.buffer_ready = False
    
    def buffer_ready_for_extraction(self):
        return self.buffer_ready

    def insert_packet(self, packet):
        print('trying to insert packet ', packet.seq_num)
        if packet.seq_num in self.valid_sequence_nums():
            self.window[packet.seq_num] = packet
            #check if the packet is a final packet type
            if packet.packet_type == packet_types.FINAL_PACKET:
                self.final_flag = True
        self.check_if_window_can_slide()

    def check_if_window_can_slide(self):
        for index in self.valid_sequence_nums():
            current_packet = self.window[index]
            if index == self.current_seq_start and current_packet != None:
                print('current sequence number is ', self.current_seq_start)
                #We know that this packet is complete, add it to the buffer
                self.buffer.append(current_packet.payload.decode('utf-8'))
                self.slide()
                if (current_packet.packet_type == packet_types.FINAL_PACKET):
                    print("all packets have been received")
                    self.buffer_ready = True

    def slide(self):
        #Reset the window so that it can receive a new packet
        self.window[self.current_seq_start] = None
        self.current_seq_start += 1
        print('sliding! new seq: ', self.current_seq_start)
    
    def valid_sequence_nums(self):
        return [num % self.max_seq_num for num in range(self.current_seq_start, self.current_seq_start + self.window_size)]

p0 = Packet(packet_type=1,seq_num=0, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p1 = Packet(packet_type=1,seq_num=1, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p2 = Packet(packet_type=1,seq_num=2, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p3 = Packet(packet_type=1,seq_num=3, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p4 = Packet(packet_type=1,seq_num=4, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p5 = Packet(packet_type=1,seq_num=5, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p6 = Packet(packet_type=1,seq_num=6, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())
p7 = Packet(packet_type=packet_types.FINAL_PACKET,seq_num=7, peer_ip_addr='localhost',peer_port=8007, payload="meh".encode())

window = RecWindow(8)
window.insert_packet(p1)
window.insert_packet(p2)
window.insert_packet(p3)
window.insert_packet(p0)
window.insert_packet(p6)
window.insert_packet(p7)
window.insert_packet(p4)
window.insert_packet(p5)