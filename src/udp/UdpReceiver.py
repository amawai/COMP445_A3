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

class UdpReceiver:
    def __init__(self, connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), router_addr="localhost", router_port=3000, peer_ip=ipaddress.ip_address(socket.gethostbyname('localhost')), peer_port=8007):
        self.connection = connection
        self.router_addr = router_addr
        self.router_port = router_port
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.timeout = 20

    #TODO: Receive packets, store in buffer, send ACKs/NAKs accordingly
    def receive(self,data):
        try:
            while True:      
                buffer = connection.recvfrom(1024)
                print (buffer)
                if buffer:  

                    seqNumber, character = buf.split(':', 1)
                    if seqNumber=='' or int(seqNumber) == 10001: 
                        cont = False
                        self.debug('Done. Closing socket.')
                        break
                    print 'Recieved: '+ buf
                    if self.packetList[int(seqNumber)] is None:
                            self.packetList[int(seqNumber)] = Packet(buf)
                    self.debug('Sending ['+seqNumber+'] ACK...')
                    connection.send(seqNumber)
                else: break                       
        finally:
            connection.close()
            self.exportResults()
               
            
    