import socket
import ipaddress
import random
from threading import Timer
from .Packet import Packet
from .PacketTypes import PacketTypes
from .AckTimer import AckTimer
from .Window import Window
from .ReceiverWindow import ReceiverWindow

packet_types = PacketTypes()
MAX_SEQUENCE_NUMBER = 10

class UdpReceiver:
    def __init__(self, connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), router_addr="localhost", router_port=3000, peer_ip=ipaddress.ip_address(socket.gethostbyname('localhost')), peer_port=8008):
        self.connection = connection
        self.router_addr = router_addr
        self.router_port = router_port
        self.peers_ip = peer_ip
        self.peer_port = peer_port
        self.timeout = 20
        self.counter = 0
        self.ack_timer = None
        self.receiver_window = ReceiverWindow(MAX_SEQUENCE_NUMBER)
        self. packet_type = packet_types.NAK
        self. packet_int = 0
        self. last_packet_index =0
        
    #TODO: Receive packets, store in buffer, send ACKs/NAKs accordingly
    def receive(self, packet, sender):
        print ("receive packet", packet.seq_num)
        if self.receiver_window.window is None: 
            self.ack_timer = AckTimer(self.timeout, self.sendPacket, self.packet_type, self.packet_int, sender)
    
        #insert packet in the window if it doesn't exist
        self.insertPacket(packet)
        if packet.packet_type == packet_types.FINAL_PACKET:
            self.receiver_window.complete  = True
            self. last_packet_index = packet.seq_num

        #check packet in window
        #valid_pkt_list =self.receiver_window.get_all_packet_in_frame()
        ''' while self.receiver_window.complete is False:
            index = 0
            for p in self.receiver_window.window:      
                if p is None:
                    if self.packet_int == ((len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER):
                        break
                    self.packet_int = ((len(self.receiver_window.buffer)+index)%MAX_SEQUENCE_NUMBER)
                    self.packet_type = packet_types.NAK
                    index+=1
                else:
                    if self.packet_int == ((len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER):
                        break
                    self.packet_int = ((len(self.receiver_window.buffer)+index)%MAX_SEQUENCE_NUMBER)
                    self.packet_type = packet_types.ACK
                    index+=1


            if self.packet_type == packet_types.ACK:
                self.packet_int = ((len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER)
         '''
        index = 0
        while index < len(self.receiver_window.window):   
            print("hello")   
            if self.receiver_window.window[index] is None:
                print("hello None") 
                if self.packet_int == (abs(len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER):
                    break
                self.packet_int = (abs(len(self.receiver_window.buffer)+index)%MAX_SEQUENCE_NUMBER)
                self.packet_type = packet_types.NAK
                index+=1
            elif self.receiver_window.window[index] is not None:
                print("hello not None") 
                if self.packet_int == (abs(len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER):
                    break
                self.packet_int = ((len(self.receiver_window.buffer)+index)%MAX_SEQUENCE_NUMBER)
                self.packet_type = packet_types.ACK
                print(packet_types.ACK)
                print(self.packet_int)
                print(self.packet_type)
                index+=1

            print(self.packet_int,self.packet_type)
            if self.packet_type == packet_types.ACK:
                #self.packet_int = ((len(self.receiver_window.buffer)+index-1)%MAX_SEQUENCE_NUMBER)
                self.sendPacket(self.packet_type,self.packet_int,sender)
            
            #check if the last packet is here
            #self.requestReady(packet, self.ack_timer)
            if self.receiver_window.complete == True :
                if(self.packet_int == self.last_packet_index):
                    self.requestReady(self.ack_timer)
           

    def requestReady(self,ack_timer):
        request =''
        #if(packet.packet_type == PacketTypes.FINAL_PACKET and temp_bool == False):
        #ack_timer.stopTimer()
            #get full request from packets
        for p in self.receiver_window.buffer:
            request += p.payload.decode("utf-8")
        self.receiver_window.complete =True
        return request
        
    def sendPacket(self, p_type,p_number,sender):   
        print("Time out, send", p_type, p_number)  
        receive_packet = Packet(packet_type= p_type,
            seq_num=p_number,
            peer_ip_addr=self.peers_ip,
            peer_port=self.peer_port,
            payload="")
        self.connection.sendto(receive_packet.to_bytes(), sender)
        if(p_type == packet_types.ACK):
            self.receiver_window.slide(p_number)
        self.resetTimer(self.ack_timer,p_number,p_type,sender)

    def insertPacket(self, packet):
        print(packet.packet_type, "packet tpyp")
        pkt_seq_num = packet.seq_num
        acked_num = len(self.receiver_window.buffer) % MAX_SEQUENCE_NUMBER
        find_p = acked_num - pkt_seq_num
        if  find_p< 0:
            find_p = MAX_SEQUENCE_NUMBER - find_p
        if  self.receiver_window.window[find_p] is None:
            self.receiver_window.window[find_p] =packet
            print(find_p)
            print (self.receiver_window.window[find_p])
        else:
            print ("duplicated packet is discarded", packet.seq_num)
       
    
    def stopTimer(self,ack_timer):
        ack_timer.stop()
        
    def resetTimer(self,ack_timer,packet_type,packet_int,sender):
        ack_timer = AckTimer(self.timeout,self.sendPacket,(packet_type,packet_int,sender))