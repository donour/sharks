#!/usr/bin/env python2
############3##################################################################
"""
Sharks LCD UI controller. Python2
"""
__author__='Donour Sizemore'

import adafruit.Adafruit_CharLCDPlate as af
import client


class Display:

    def __init__(self):
        self.lcd = af.Adafruit_CharLCDPlate()
        self.refresh()

    def set_startup(self):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.RED)

    def disable(self):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.OFF)
        
    def refresh(self, line2="---"):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.GREEN)
        line1 = datetime.datetime.now().strftime("%H:%M:%S")
        self.lcd.message(line1 + "\n" + line2)

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
    d.set_startup()
    time.sleep(1)

    host = "192.168.0.1"
    cli = client.recv_server(host)


    while True:
        freq = 10
        cli.register(host)
        for i in range(0,freq):
            sample = cli.get_sample()
            if(sample != None):
                print sample
                d.refresh("%.5f" % sample)
            buttons = d.buttons()
            if len(buttons) > 0:
                if d.lcd.SELECT in buttons:
                    d.disable()
            time.sleep(1.0/freq)
