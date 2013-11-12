#!/usr/bin/env python3

import sys
import ride_height
import transmitter
from registration import reg_server

UPDATE_FREQ = 20.0
REG_TIME = 60.0 # seconds
PORT = 55555

if __name__ == "__main__":
    import time

    reg_port = PORT+1
    lf = transmitter.Transmitter("LF")
    lr = transmitter.Transmitter("LR")
    rf = transmitter.Transmitter("RF")
    rr = transmitter.Transmitter("RR")
    r = reg_server('192.168.0.1', reg_port)

    clients = {}
    
    while True:
        hosts = r.get_hosts()


        for host in hosts:
            clients[host] = time.time()+ REG_TIME
            s = host + ":" + str(clients[host]) # 
            print(s)
            

        now = time.time()
        h = ride_height.height()
        for host in clients.keys():
            if now < clients[host]:
                lf.send([host], int(now*1000), 0, h)
                lr.send([host], int(now*1000), 0, h)
                rf.send([host], int(now*1000), 0, h)
                rr.send([host], int(now*1000), 0, h)            
                sys.stdout.write(".");sys.stdout.flush()
        time.sleep(1.0/UPDATE_FREQ)
