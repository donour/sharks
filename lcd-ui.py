#!/usr/bin/env python2
############3##################################################################
"""
Sharks LCD UI controller. Python2
"""
__author__='Donour Sizemore'

import Adafruit_CharLCDPlate as af

class Display:

    def __init__(self):

        self.lcd = af.Adafruit_CharLCDPlate()

    def refresh(self):
        self.lcd.clear()

        line1 = datetime.datetime.now().strftime("%H:%M:%S")
        line2 = "RPI"
        d.lcd.message( line1 + "\n" + line2)

    def buttons(self):
        """
        Poll all hardware buttons and return list of active buttons
        """
        result = []
        btns = [self.lcd.SELECT, self.lcd.LEFT, self.lcd.UP, self.lcd.DOWN, self.lcd.RIGHT]
        for b in btns:
            r = self.lcd.buttonPressed(b)
            if r != 0:
                result.append(b)

        return result
    
if __name__ == "__main__":
    import datetime,time

    d = Display()
    while True:
        d.refresh()
        buttons = d.buttons()
        if len(buttons) > 0:
            print buttons
        time.sleep(0.1)
        
