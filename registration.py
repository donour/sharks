#!/usr/bin/env python3
__author__= 'Donour Sizemore'

import socketserver

hosts = []

class SharksRegistrationHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global hosts
        hosts.append(self.client_address[0])

class reg_server:

    def __init__(self, host, port):
        self.sock = socketserver.UDPServer( (host, port), SharksRegistrationHandler)
        self.sock.timeout = 0.0

    def get_hosts(self):
        global hosts
        hosts = []
        self.sock.handle_request()

        return hosts
    
if __name__ == "__main__":
    import time, sys
    PORT = 55556
    host = '192.168.0.1'

    s = reg_server(host, PORT)

    while True:
        
        time.sleep(0.05)
        print(s.get_hosts())
        sys.stdout.write('.')
        sys.stdout.flush()
