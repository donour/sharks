#!/usr/bin/env python2
###############################################################################
__author__ = 'Donour Sizemore'

import lcdui
import sys

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s <message>" % sys.argv[0]
        sys.exit(-1)
        
    d = lcdui.Display()
    d.lcd.clear()
    d.lcd.backlight(d.lcd.RED)
    d.lcd.message(sys.argv[1])
    
