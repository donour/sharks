#!/usr/bin/python

import random

def height():

    return random.random()

if __name__ == "__main__":
    import sys,time
    while True:
        s = "\r%.3f" % height()
        sys.stdout.write(s)
        time.sleep(0.1)

