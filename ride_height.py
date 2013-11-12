#!/usr/bin/python

import random

start = 0.0
def height():
    global start
    start += 0.01
    return start

if __name__ == "__main__":
    import sys,time
    while True:
        s = "\r%.3f" % height()
        sys.stdout.write(s)
        time.sleep(0.1)

