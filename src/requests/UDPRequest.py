from abc import ABC, abstractmethod
from urllib.parse import urlsplit
import re
import socket
import ipaddress
from udp.UdpTransporter import UdpTransporter

class UDPRequest(ABC):
    def __init__(self, url, port, write_file, headers=[], verbose=False):
        self.url = url
        self.port = port
        self.headers = headers
        self.verbose = verbose
        self.connection = None
        self.write_file = write_file

    @abstractmethod
    def create_request(self, path, query, host):
        return

    def execute(self, redirected=0):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        url_splitted = urlsplit(self.url)
        host = url_splitted.netloc
        port = self.port if ":" not in host else int(host[host.index(":") + 1:])
        self.port = port
        host = host if ":" not in url_splitted.netloc else host[0:host.index(":")]
        path = url_splitted.path
        query = url_splitted.query
        query = "" if not query else "?" + query
        request = self.create_request(path, query, host)

        try:
            result = self.send_request(request)
            redirection = self.process_response(result)
            if (redirection):
                if (redirected < 5):
                    self.execute(redirected + 1)
                else:
                    print("Too many redirections, operation aborted")
        finally:
            self.connection.close()

    def send_request(self, request):
        udp = UdpTransporter()
        #TODO: udp.send(request) doesn't actually send a response
        response = udp.send(request)
        
        return response
    

    def process_response(self, result):
        response = ""
        #TODO: Uncomment once udp.send() returns a response
        # while (len(result) > 0):
        #     response += result.decode("utf-8")
        #     #result = self.connection.recv(10000)
        # status_code = re.findall(r"(?<=HTTP\/\d\.\d )(\d\d\d)", response)
        # if (len(status_code) >= 1):
        #     status_code = int(status_code[0])
        # if (status_code == 302):
        #     self.redirect(response)
        #     return True
        # else:
        #     self.display_response(response)
        #     return False
        return False

    def redirect(self, response):
        location = re.findall(r"(?<=Location\: )(.*)", response)
        if (len(location) > 0):
            location_str = str(location[0]).replace("\r", "")
            self.url = location_str
        else:
            print("Failed to find new url location")

    def display_response(self, response):
        response_string = ""
        if (self.verbose):
            response_string = response
        else:
            response_string = response[response.find("\r\n\r\n") + 1:]
        if self.write_file is not None:
            f = open(self.write_file, "w")
            f.write(response_string)
            f.close()
            print("The response is in the file " + self.write_file)
        else:
            print(response_string)
