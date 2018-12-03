from requests import GetRequest
from requests import PostRequest

class HttpcClient:
    @staticmethod
    def execute_get_request(args):
        url = args.URL
        headers = args.header or []
        verbose = False
        if (args.verbose):
            verbose = True

        writefile = args.writefile
        router_host = args.routerHost
        router_port = args.routerPort
        get_request = GetRequest(url, 80, writefile, router_port, router_host,  headers, verbose)
        get_request.execute()
    
    @staticmethod
    def execute_post_request(args):
        url = args.URL
        headers = args.header or []
        verbose = False
        if (args.verbose):
            verbose = True

        data = args.data
        file = args.file
        writefile = args.writefile
        router_host = args.routerHost
        router_port = args.routerPort

        if (bool(data) != bool(file)):
            post_request = PostRequest(url, 80, data, file, writefile, router_port, router_host, headers, verbose)
            post_request.execute()
        else:
            raise ValueError("For POST request, use either -f or -d")
        pass
