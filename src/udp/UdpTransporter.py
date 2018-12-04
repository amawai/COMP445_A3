import socket
import ipaddress
import random
import sys
from threading import Timer
from .Window import Window
from .Packet import Packet
from .DataConverter import DataConverter
from .PacketTypes import PacketTypes
from .RecWindow import RecWindow

packet_types = PacketTypes()
MAX_SEQUENCE_NUMBER = 10
 
class UdpTransporter:
    def __init__(self, timeout, connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), router_addr="localhost", router_port=3000, peer_ip=ipaddress.ip_address(socket.gethostbyname('localhost')), peer_port=8008):
        self.connection = connection
        self.router_addr = router_addr
        self.router_port = router_port
        self.peer_ip = ipaddress.ip_address(socket.gethostbyname(peer_ip)) if peer_ip == "localhost" else peer_ip
        self.peer_port = peer_port
        self.timeout = timeout
        self.stop_all_timers = False
        self.keep_alive_num = 25

    def init_handshake(self):
        initial_seq_num = random.randrange(0, 2**31)
        syn_packet = Packet(packet_type=packet_types.SYN,
                   seq_num=initial_seq_num,
                   peer_ip_addr=self.peer_ip,
                   peer_port=self.peer_port,
                   payload='')
        received_syn_ack = False
        timeout_count = 0
        while (not received_syn_ack):
            try:
                self.send_packet(syn_packet)
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
                timeout_count += 1
                print("Timeout, resending...")
                if self.keep_alive_counter(timeout_count) is False:
                    sys.exit()
                else:
                    continue

    #This is called if SYN type packet is received
    def handshake_receive(self, packet, sender):
        random_seq_num = random.randrange(0, 2**31)
        ack_num = str(packet.seq_num + 1).encode("utf-8")
        syn_ack_packet = Packet(packet_type=packet_types.SYN_ACK,
                        seq_num=random_seq_num,
                        peer_ip_addr=packet.peer_ip_addr,
                        peer_port=packet.peer_port,
                        payload=ack_num)
        self.connection.sendto(syn_ack_packet.to_bytes(), sender)

    def send(self, data):
        self.complete_sending = False
        packets = DataConverter.convert_data_to_packets(packet_types.DATA, self.peer_ip, self.peer_port, data, MAX_SEQUENCE_NUMBER)
        window = Window(packets, MAX_SEQUENCE_NUMBER)
        frame_timers = {}
        self.send_all_window_frames(window, frame_timers)
        no_response = False
        timeout_count = 0
        while(not window.complete or no_response):
            try:
                if self.connection == None:
                    break
                else:
                    response, sender = self.connection.recvfrom(1024)
                    p = Packet.from_bytes(response)
                    print('RECEIVED ' + packet_types.get_packet_name(p.packet_type) + str(p.seq_num))
                    if p.packet_type == packet_types.ACK:
                        completed_frames = window.slide_window(p.seq_num)
                        #print('THESE WERE COMPLETED')
                        #print(completed_frames)
                        self.stop_timer(frame_timers, completed_frames)
                        self.send_all_window_frames(window, frame_timers)
                    elif p.packet_type == packet_types.NAK:
                        completed_frames = window.slide_window((p.seq_num - 1) % MAX_SEQUENCE_NUMBER)
                        self.stop_timer(frame_timers, completed_frames)
                        #resend the packet with the corresponding sequence number
                        self.send_packet(window.get_window_data(p.seq_num))
                        if p.seq_num in frame_timers:
                            self.create_timer_for_packet([frame_timers[p.seq_num]])
                    elif p.packet_type == packet_types.FINAL_REC_PACKET:
                        window.complete = True
                        print("All packets sent successfully")
                        break;
            except socket.timeout:
                if not no_response:
                    timeout_count += 1
                    print("Sending timeout, resending...")
                    self.send_all_window_frames(window, frame_timers)
                    if self.keep_alive_counter(timeout_count) is False:
                        no_response = True
                        break
                    else:
                        continue
        self.stop_all_timers = True
        return False if no_response else True

    def receive_response(self):
        rec_window = RecWindow()
        timeout_count = 0
        while not rec_window.buffer_ready_for_extraction():
            try:
                if (self.connection == None):
                    break
                response, sender = self.connection.recvfrom(1024)
                p = Packet.from_bytes(response)
                if (p.packet_type in [packet_types.DATA, packet_types.FINAL_SEND_PACKET]):
                    print('RECEIVED ' + packet_types.get_packet_name(p.packet_type) + str(p.seq_num))
                    packet_type, seq_num = rec_window.insert_packet(p)
                    packet_to_send = Packet(
                        packet_type=packet_type,
                        seq_num=seq_num,
                        peer_ip_addr=p.peer_ip_addr,
                        peer_port=p.peer_port,
                        payload=''
                    )
                    self.send_packet(packet_to_send)
            except socket.timeout:
                timeout_count += 1
                print("Receive timeout, resending...")
                if self.keep_alive_counter(timeout_count) is False:
                    sys.exit()
                else:
                    continue
        return rec_window.extract_buffer()

    def send_packet(self, packet):
        if packet != None:
            print('SENDING ' + packet_types.get_packet_name(packet.packet_type) + '#' + str(packet.seq_num))
            if self.connection != None:
                self.connection.sendto(packet.to_bytes(), (self.router_addr, self.router_port))
                self.connection.settimeout(self.timeout)

    def send_all_window_frames(self, window, frame_timers):
        for p in window.get_all_window_data():
            if p is not None:
                seq_num = p.seq_num
                frame_timers[seq_num] = {"packet": p, "acknowledged": False}
                self.create_timer_for_packet([frame_timers[seq_num]])
                self.send_packet(p)

    def stop_timer(self, frame_timers, frames):
        for frame in frames:
            if frame in frame_timers:
                frame_timers[frame]['acknowledged'] = True
    
    def manage_timer(self, frame_info):
        if not self.stop_all_timers:
            packet = frame_info['packet']
            acknowledged = frame_info['acknowledged']
            if not acknowledged:
                self.send_packet(packet)
    
    def create_timer_for_packet(self, frame_info):
        Timer(self.timeout, self.manage_timer, frame_info).start()
    
    def keep_alive_counter(self, timeout_count):
        if timeout_count == self.keep_alive_num:
            print("No response. Quitting...")
            return False