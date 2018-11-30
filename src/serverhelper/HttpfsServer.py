import socket
import threading
from .RequestHandler import RequestHandler
from .ResponseCreator import ResponseCreator
from udp.PacketTypes import PacketTypes
from udp.Packet import Packet
from udp.UdpTransporter import UdpTransporter
import datetime

REQUEST_TYPE = 0
packet_types = PacketTypes()

class HttpfsServer:
    def __init__(self, verbose, port, directory):
        self.verbose = verbose
        self.port = port
        self.directory = directory
        self.clients = {}
    
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

        elif p.packet_type in [packet_types.DATA]:
            udpTransporter = self.clients[peer]
            request = udpTransporter.receive()
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