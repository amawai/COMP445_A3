mport socket
import threading
from .RequestHandler import RequestHandler
from .ResponseCreator import ResponseCreator
from udp.UdpTransporter import UdpTransporter
import datetime

REQUEST_TYPE = 0
class HttpfsServer:
    def __init__(self, verbose, port, directory):
        self.verbose = verbose
        self.port = port
        self.directory = directory
    
    def start(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listener.bind(('', self.port))
            listener.listen(5)
            if (self.verbose):
                print('httpfs server is listening at ', self.port)
            while True:
                conn, addr = listener.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                #data, sender = listener.recvfrom(1024)
                #threading.Thread(target=self.handle_client, args=(listener, data, sender)).start()
        finally:
            listener.close()
    
    def handle_client(self, conn, addr):
        #receive request, use sliding window
        request = conn.recv(1024).decode("utf-8")
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
            
            udpTransporter = UdpTransporter()
            udpTransporter.send(http_response)