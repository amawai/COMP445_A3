import argparse
import socket
import random

from Packet import Packet

def run_server(port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()

def handshake_receive(conn, data, sender):
    try:
        random_seq_num = random.randrange(0, 2**31)
        p = Packet.from_bytes(data)
        p.packet_type = 4
        #The ack num
        next_seq = int(p.seq_num + 1)
        p.payload =  str(next_seq).encode("utf-8")
        p.seq_num = random_seq_num

        conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("Error: ", e)

def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print(sender)
        print("Router: ", sender)

        print("Router0: ", sender[0])
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))
        print("Packet seq: ", p.seq_num)
        if (p.packet_type == 3):
                handshake_receive(conn, data, sender)
        else:
                p.packet_type = 1
                conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("Error: ", e)


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server(args.port)
