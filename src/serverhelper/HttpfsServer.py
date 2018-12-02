import socket
import threading
from .RequestHandler import RequestHandler
from .ResponseCreator import ResponseCreator
from udp.PacketTypes import PacketTypes
from udp.Packet import Packet
from udp.UdpTransporter import UdpTransporter
from udp.RecWindow import RecWindow
import datetime

REQUEST_TYPE = 0
packet_types = PacketTypes()

class HttpfsServer:
    def __init__(self, verbose, port, directory):
        self.verbose = verbose
        self.port = port
        self.directory = directory
        self.clients = {}
        self.receiver_windows = {}
    
    def start(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            listener.bind(('', self.port))
            if (self.verbose):
                print('httpfs server is listening at ', self.port)
            while True:
                data, sender = listener.recvfrom(1024)
                self.handle_client(listener, data, sender)
                #TODO: Multi clients
                #threading.Thread(target=self.handle_client, args=(listener, data, sender)).start()
        finally:
            listener.close()
    
    def handle_client(self, conn, data, sender):
        p = Packet.from_bytes(data)
        peer ="%s:%s" % (p.peer_ip_addr, p.peer_port)
        if (p.packet_type == packet_types.SYN):
            udpTransporter = UdpTransporter(conn)
            udpTransporter.handshake_receive(p, sender)
            self.clients[peer] = udpTransporter

        elif p.packet_type in [packet_types.DATA, packet_types.FINAL_PACKET]:
            udpTransporter = None
            if peer in self.clients:
                udpTransporter = self.clients[peer]
            else:
                udpTransporter = UdpTransporter(conn)
            if not peer in self.receiver_windows:
                self.receiver_windows[peer] = RecWindow()
            rec_window = self.receiver_windows[peer]
            packet_to_send = self.receive(conn, sender, p, rec_window)
            while not rec_window.buffer_ready_for_extraction():
                try:
                    response, sender = conn.recvfrom(1024)
                    p = Packet.from_bytes(response)
                    packet_to_send = self.receive(conn, sender, p, rec_window)
                except socket.timeout:
                    conn.sendto(packet_to_send.to_bytes(), sender)
                    continue
            if rec_window.buffer_ready_for_extraction():
                completed_packet = Packet(
                    packet_type=packet_types.FINAL_PACKET,
                    seq_num=0,
                    peer_ip_addr=p.peer_ip_addr,
                    peer_port=p.peer_port,
                    payload=''
                )
                conn.sendto(completed_packet.to_bytes(), sender)
                request = rec_window.extract_buffer()
                #Reset the receiver
                self.receiver_windows[peer] = RecWindow()
                if (self.verbose):
                    print(request)
                request_array = request[0:request.index('\r\n\r\n')].split()
                request_body = request[request.index('\r\n\r\n'):].replace('\r\n\r\n', '')
                request_type = request_array[REQUEST_TYPE]
                response = ''
                try:
                    response = {}
                    if (request_type.lower() == 'get'):
                        response = RequestHandler(request_array, self.directory, request_body).process_get()
                    elif (request_type.lower() == 'post'):
                        response = RequestHandler(request_array, self.directory, request_body).process_post()
                except:
                    response = {'status': 500, 'content': ''}
                finally:
                    http_response = ResponseCreator.create_response(response['status'], response['content'], response['mimetype'])
                    if (self.verbose):
                        print(http_response)
                    udpTransporter.send(http_response)

    def receive(self, conn, sender, packet, window):
        packet_type, seq_num = window.insert_packet(packet)
        packet_to_send = Packet(
            packet_type=packet_type,
            seq_num=seq_num,
            peer_ip_addr=packet.peer_ip_addr,
            peer_port=packet.peer_port,
            payload=''
        )
        conn.sendto(packet_to_send.to_bytes(), sender)
        return packet_to_send