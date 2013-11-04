#!/usr/bin/env python3

import ride_height
import transmitter

if __name__ == "__main__":
    import time
    
    t = transmitter.Transmitter("LF")

    while True:
        hosts = ['172.16.8.151', '172.16.8.93']
        h = ride_height.height()

        t.send(hosts, int(time.time()*1000), 0, h)
        time.sleep(0.01)
