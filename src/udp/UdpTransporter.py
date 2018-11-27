import socket
import ipaddress
from .Window import Window
from .Packet import Packet
from .DataConverter import DataConverter
from .PacketTypes import PacketTypes

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
    
    def send(self, data):
        packets = DataConverter.convert_data_to_packets(packet_types.DATA, self.peer_ip, self.peer_port, data, MAX_SEQUENCE_NUMBER)
        window = Window(packets, MAX_SEQUENCE_NUMBER)
        while(not window.complete):
            for p in window.get_all_window_data():
                if p is not None:
                    print("SENDING: ", p.payload.decode('utf-8'))
                    self.send_packet(p)
            try:
                response, sender = self.connection.recvfrom(1024)
                p = Packet.from_bytes(response)
                print("RECEIVED: ", p.payload.decode('utf-8'))
                if p.packet_type == packet_types.ACK:
                    window.slide_window(p.seq_num)
                #TODO: test the nak
                elif p.packet_type == packet_types.NAK:
                    #resend the packet with the corresponding sequence number
                    self.send_packet(window.get_window_data(p.seq_num))
            except socket.timeout:
                print("Timeout, resending...")
                continue

        self.connection.close()
        #TODO: Actual return, we simply return true for now
        return True
    
    #TODO: Receive packets, store in buffer, send ACKs/NAKs accordingly
    def receive(self):
        pass

    def send_packet(self, packet):
        self.connection.sendto(packet.to_bytes(), (self.router_addr, self.router_port))
        self.connection.settimeout(self.timeout)
                    
    

    

    
