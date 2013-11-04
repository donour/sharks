#!/usr/bin/python
###############################################################################
"""
Shark transmission protocol implementation
"""
__author__ = 'Donour Sizemore'

import socket

class Transmitter:
    def __init__(self, port = 55555):
        self.seqnum = 0
        self.port = port
        
    def send(self, host_list, timestamp, weight, height): 
        msgstring = "--,SHARKNET1, %s, %d, %d, %.3f,--,--,--,--,--,--" %\
                    (timestamp, self.seqnum, weight, height)
        msg = bytes(msgstring,'UTF-8')
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for addr in  host_list:
            sock.sendto(msg, (addr, self.port))

        self.seqnum = self.seqnum + 1

if __name__ == "__main__":
    import time
    t = Transmitter()
    t.send(['172.16.8.151', '127.0.0.1'], str(time.time()*1000), 0, 0.0)
