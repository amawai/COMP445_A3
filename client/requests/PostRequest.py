import mimetypes
from .UDPRequest import UDPRequest

class PostRequest(Request):
    def __init__(self, url, port, data, file, write_file, headers=[], verbose=False):
        super().__init__(url, port, write_file, headers, verbose)
        self.data = data
        self.file = file

    def create_request(self, path, query, host):
        request = "POST " + path + query + " HTTP/1.0\r\nHost: " + host
        for header in self.headers:
            request += "\r\n" + header
        if self.data is not None:
            request += "\r\nContent-Length: " + str(len(self.data))
            request += "\r\n\r\n" + self.data
        elif self.file is not None:
            f = open(self.file, 'r')
            f_data = f.read()
            f.close()
            request += "\r\nContent-Type:" + (mimetypes.guess_type(self.file)[0] or "application/json")
            request += "\r\nContent-Length: " + str(len(f_data))
            request += "\r\n\r\n" + f_data
        request += "\r\n\r\n"
        return request
