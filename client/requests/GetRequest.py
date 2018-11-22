from .UDPRequest import UDPRequest

class GetRequest(Request):
    def __init__(self, url, port, write_file, headers=[], verbose=False):
        super().__init__(url, port, write_file, headers, verbose)

    def create_request(self, path, query, host):
        request = "GET "+ path + query + " HTTP/1.1\r\nHost: " + host + ":" + str(self.port)
        for header in self.headers:
            request += "\r\n" + header
        request += "\r\n\r\n"
        return request