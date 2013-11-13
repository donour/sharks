#!/usr/bin/env python3
###############################################################################
__author__ = 'Donour Sizemore'

import SocketServer, socket

PROTOCOL_VERSION="1.0"
VERBOSITY = 99

last_msg = None

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
        if VERBOSITY > 0:
            print "i: Registering:", host
        self.reg_sock.sendto("HELO", (host,self.port+1))

    def get_sample(self):      
        res = None

        global last_msg
        last_msg = ""
        while last_msg is not None:
            last_msg = None
            self.sock.handle_request()
            if last_msg is not None:
                vals = last_msg.split(',')
                if len(vals) > 6:
                    try:
                        res =float(vals[6])
                    except:
                        res = None

        return res
    
if __name__ == "__main__":
    host = "192.168.0.1"
    s = recv_server(host)

    import time
    while True:
        freq = 100
        for i in range(0,freq):
            r = s.get_sample()
            if r is not None: print r
            time.sleep(1.0/freq)           
        s.register(host)

    
