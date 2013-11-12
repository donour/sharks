#!/usr/bin/env python3
###############################################################################

import SocketServer, socket

PROTOCOL_VERSION="1.0"
VERBOSITY = 99

class SharksDataHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print self.client_address[0]

class recv_server:

    def __init__(self, host, port = 55555):
        self.port = port
        self.sock = SocketServer.UDPServer( (host, port), SharksDataHandler)
        self.sock.timeout = 0.0

        self.reg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def register(self, host):
        print "sending"
        self.reg_sock.sendto("HELO", (host,self.port+1))
    
if __name__ == "__main__":
    host = "192.168.0.1"
    s = recv_server(host)

    import time
    while True:
        s.register(host)
        time.sleep(1)
    
