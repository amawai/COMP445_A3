import argparse
import sys
from serverhelper import HttpfsServer

class httpfs(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='An implementation of HTTP server library')
        #parser.add_argument('command', help='Subcommand to run')
        parser.add_argument("-v", "--verbose", help="print debug messages",  action="store_true")
        parser.add_argument("-p", "--port", help="Specifies the port number that the server will listen and serve at", default=8080, type=int)
        parser.add_argument("-d", "--directory", help="Specifies the directory that the server will use to read/write quested files. Default is the current directory when launching the application", default='public')
        parser.add_argument("-rp","--routerPort", help="Port number of Router", default=3000, type=int)
        parser.add_argument("-rh","--routerHost", help="Host of router",default='localhost')
        args = parser.parse_args(sys.argv[1:])
        server = HttpfsServer(args.verbose, args.port, args.directory)
        server.start()
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()



if __name__ == '__main__':
    httpfs()