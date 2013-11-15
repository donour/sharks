#!/usr/bin/env python3

import sys
import ride_height
import transmitter
from registration import reg_server

UPDATE_FREQ = 20.0
REG_TIME = 60.0 # seconds
PORT = 55555

VERBOSITY = 0

if __name__ == "__main__":
    import time, sys

    if len(sys.argv) < 3:
        print("usage: %s <CORNER ID> <ip address>" % sys.argv[0])
        sys.exit(-1)
    else:
        corner = sys.argv[1]
        addr = sys.argv[2]
    
    reg_port = PORT+1
    t = transmitter.Transmitter(corner)
    r = reg_server(addr, reg_port)

    clients = {}
    
    while True:
        hosts = r.get_hosts()


        for host in hosts:
            clients[host] = time.time()+ REG_TIME
            s = host + ":" + str(clients[host]) 
            if VERBOSITY > 1:
                print(s)
            

        now = time.time()
        h = ride_height.height()
        for host in clients.keys():
            if now < clients[host]:
                t.send([host], int(now*1000), 0, h)
                if VERBOSITY > 1:
                    sys.stdout.write(".");sys.stdout.flush()
        time.sleep(1.0/UPDATE_FREQ)
