import socket
import ipaddress
import random
from threading import Timer
from .Window import Window
from .Packet import Packet
from .DataConverter import DataConverter
from .PacketTypes import PacketTypes
from .FrameTimer import FrameTimer

packet_types = PacketTypes()
MAX_SEQUENCE_NUMBER = 10

class UdpTransporter:
    def __init__(self, connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), router_addr="localhost", router_port=3000, peer_ip=ipaddress.ip_address(socket.gethostbyname('localhost')), peer_port=8007):
        self.connection = connection
        self.router_addr = router_addr
        self.router_port = router_port
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.timeout = 20
        self.handshake_sender()

    def handshake_sender(self):
        initial_seq_num = random.randrange(0, 2**31)
        syn_packet = Packet(packet_type=packet_types.SYN,
                   seq_num=initial_seq_num,
                   peer_ip_addr=self.peer_ip,
                   peer_port=self.peer_port,
                   payload='')
        received_syn_ack = False
        while (not received_syn_ack):
            self.send_packet(syn_packet)
            try:
                response, sender = self.connection.recvfrom(1024)
                p = Packet.from_bytes(response)
                if p.packet_type == packet_types.SYN_ACK:
                    next_seq_num = int(p.seq_num) + 1
                    ack_packet = Packet(packet_type=packet_types.ACK,
                                seq_num=next_seq_num,
                                peer_ip_addr=self.peer_ip,
                                peer_port=self.peer_port,
                                payload='')
                    self.send_packet(ack_packet)
                    received_syn_ack = True
            except socket.timeout:
                continue
    
    #This is called if SYN type packet is received 
    def handshake_receive(self, data, sender):
        p = Packet.from_bytes(data)
        random_seq_num = random.randrange(0, 2**31)
        ack_num = str(p.next_seq + 1).encode("utf-8")
        p = Packet.from_bytes(data)
        syn_ack_packet = Packet(packet_type=packet_types.SYN_ACK,
                        seq_num=random_seq_num,
                        peer_ip_addr=sender[0],
                        peer_port=sender[1],
                        payload=ack_num)
        self.connection.sendto(p.to_bytes(), sender)
    

    def send(self, data):
        packets = DataConverter.convert_data_to_packets(packet_types.DATA, self.peer_ip, self.peer_port, data, MAX_SEQUENCE_NUMBER)
        print(packets)
        window = Window(packets, MAX_SEQUENCE_NUMBER)
        frame_timers = {}
        self.send_all_window_frames(window, frame_timers)
        while(not window.complete):
            try:
                response, sender = self.connection.recvfrom(1024)
                p = Packet.from_bytes(response)
                if p.packet_type == packet_types.ACK:
                    completed_frames = window.slide_window(p.seq_num)
                    print('THESE WERE COMPLETED')
                    print(completed_frames)
                    self.stop_timer(frame_timers, completed_frames)
                    self.send_all_window_frames(window, frame_timers)
                elif p.packet_type == packet_types.NAK:
                    #resend the packet with the corresponding sequence number
                    self.send_packet(window.get_window_data(p.seq_num))
                    self.reset_timer(frame_timers, p)
            except socket.timeout:
                print("Timeout, resending...")
                self.send_all_window_frames(window, frame_timers)
                continue
        self.stop_all_timers(frame_timers)
        self.connection.close()
        #TODO: Actual return, we simply return true for now
        return True
    
    #TODO: Receive packets, store in buffer, send ACKs/NAKs accordingly
    def receive(self):
        pass

    def send_packet(self, packet):
        if packet != None:
            self.connection.sendto(packet.to_bytes(), (self.router_addr, self.router_port))
            self.connection.settimeout(self.timeout)

    def send_all_window_frames(self, window, frame_timers):
        print("Valid window frames")
        print(window.valid_sequence_nums())
        for p in window.get_all_window_data():
            if p is not None:
                print("SENDING: #", p.seq_num)
                seq_num = p.seq_num
                if p.seq_num in frame_timers:
                    frame_timers[seq_num].stop()
                frame_timers[seq_num] = FrameTimer(self.timeout, self.send_packet, p)
                self.send_packet(p)

    def stop_all_timers(self, frame_timers):
        for timer in frame_timers.values():
            timer.stop()

    def stop_timer(self, frame_timers, frames):
        for frame in frames:
            if frame in frame_timers:
                frame_timers[frame].stop()

    def reset_timer(self, frame_timers, packet):
        if frame in frame_timers:
            frame_timers[frame].stop()
        frame_timers[packet.seq_num] = FrameTimer(self.timeout, self.send_packet, packet)
    

    

    
