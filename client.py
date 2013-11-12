#!/usr/bin/env python3
###############################################################################

import SocketServer, socket

PROTOCOL_VERSION="1.0"
VERBOSITY = 99

last_msg = ""

class SharksDataHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global last_msg
        last_msg = self.request[0].strip()

class recv_server:

    def __init__(self, host, port = 55555):
        self.port = port
        self.sock = SocketServer.UDPServer( (host, port), SharksDataHandler)
        self.sock.timeout = 0.0

        self.reg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def register(self, host):
        print "sending"
        self.reg_sock.sendto("HELO", (host,self.port+1))

    def get_sample(self):
        self.sock.handle_request()
        
if __name__ == "__main__":
    host = "192.168.0.1"
    s = recv_server(host)

    import time
    while True:
        freq = 100
        for i in range(0,freq):
            s.get_sample()
            if last_msg is not None:
                print last_msg
                last_msg = None
            time.sleep(1.0/freq)           
        s.register(host)

    
