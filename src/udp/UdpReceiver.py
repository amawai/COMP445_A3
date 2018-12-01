import socket
import ipaddress
import random
from threading import Timer
from .Packet import Packet
from .PacketTypes import PacketTypes
from .AckTimer import AckTimer

packet_types = PacketTypes()
MAX_SEQUENCE_NUMBER = 10

class UdpReceiver:
    def __init__(self, connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), router_addr="localhost", router_port=3000, peer_ip=ipaddress.ip_address(socket.gethostbyname('localhost')), peer_port=41830):
        self.connection = connection
        self.router_addr = router_addr
        self.router_port = router_port
        self.peers_ip = peer_ip
        self.peer_port = peer_port
        self.timeout = 20
        self.buffer = []
        self.pointer = 0
        self.ack_timer

    #TODO: Receive packets, store in buffer, send ACKs/NAKs accordingly
    def receive(self, packet, sender):
        packet_type = 'NAK'
        packet_int =0
        index = 0
        if not self.buffer: 
            self.ack_timer = AckTimer(self.timeout,self.sendPacket,(packet_type,packet_int))
    
        #insert packet in the buffer if it doesn't exist
        self.insertPacket(packet)
       
        #check packet in buffer
        for index in range(len(self.buffer)):
            if not self.buffer[index]:  # if packet doesnot exist in the buffer
                if packet_int == index-1:
                    packet_type = 'NAK'
                    break
                packet_int =index
                index +=1
            else:# if packet exists in the buffer
                index +=1

        if index == len(self.buffer):
            packet_type = 'ACK'
            packet_int =index -1

        #check if the last packet is here
        self.requestReady(packet, self.ack_timer)
        

    def requestReady(self, packet,ackTimer ):
        request =''
        if(packet.packet_type == PacketTypes.FINAL_PACKET and self.pointer == packet.seq_num):
            ackTimer.stopTimer()
            #get full request from packets
            for p in self.buffer:
                request += p.payload
            return request

    def slidePointer(self, packet_type,packet_int):
        if packet_type == PacketTypes.ACK:
            self.pointer = packet_int+1
        elif packet_type == PacketTypes.NAK:
            self.pointer = packet_int-1
        
    def sendPacket(self, p_type,p_number,sender):     
        receive_packet = Packet(packet_type= p_type,
            seq_num=p_number,
            peer_ip_addr=self.peers_ip,
            peer_port=self.peer_port,
            payload="")
        self.connection.sendto(receive_packet.to_bytes(), sender)
        self.slidePointer(p_type,p_number)
        self.resetTimer(self.ack_timer,p_number,p_type)

    def insertPacket(self, packet):
        insert_seq_num = packet.seq_num
        for p in self.buffer:
            if p.seq_num == insert_seq_num:
                break
            elif p.seq_num is not insert_seq_num:
                self.buffer.insert(insert_seq_num,packet)

    
    def stopTimer(self,ack_timer):
        ack_timer.stop()
        
    def resetTimer(self,ack_timer,packet_type,packet_int):
        ack_timer = AckTimer(self.timeout,self.sendPacket,(packet_type,packet_int))