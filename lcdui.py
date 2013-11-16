#!/usr/bin/env python2
############3##################################################################
"""
Sharks LCD UI controller. Python2
"""
__author__='Donour Sizemore'

import time, datetime
import os
import adafruit.Adafruit_CharLCDPlate as af
import client

VERBOSITY = 0
class Display:

    def __init__(self, header = "MWRSCALE"):
        self.header = header
        self.lcd = af.Adafruit_CharLCDPlate()
        self.refresh()

    def set_startup(self):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.RED)

    def disable(self):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.OFF)
        
    def refresh(self, line2="---", status = ""):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.GREEN)
        line1 = self.header + status
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

    def settings_menu(self, options = ['option1', 'option2', 'option3']):
        done = False
        selected_option = 0
        while done == False and len(options) > 0:
            self.lcd.backlight(self.lcd.BLUE)
            self.lcd.clear()

            line1 = "SelectConfig  +-"
            line2 = options[selected_option % len(options)]
            self.lcd.message(line1 + "\n" + line2)
            
            buttons = self.buttons()
            if self.lcd.SELECT in buttons:
                done = True
            elif self.lcd.UP in buttons:
                selected_option += 1
            elif self.lcd.DOWN in buttons:
                selected_option -= 1

            time.sleep(0.1)

        return options[selected_option % len(options)]
    
if __name__ == "__main__":
    config_dir = '/sharks.configs'
    
    freq = 6 # display update frequency

    fd = file("/etc/sharks.header", "r");
    header = fd.read().strip()

    config_options = os.listdir(config_dir)

    d = Display(header)
    d.set_startup()

    host = "192.168.0.1"
    cli = client.recv_server(host)

    status_animation = ["<( 0-0 )>"," (>0-0 )>"," (>0-0<) ","<( 0-0<) " ]  
    animation_count = 0
    while True:
        cli.register(host)
        for i in range(0,freq):
            sample = cli.get_sample()
            if(sample != None):
                if VERBOSITY > 0:
                    print sample
                d.refresh(str(sample), status_animation[animation_count])
            buttons = d.buttons()
            if len(buttons) > 0:
                if d.lcd.RIGHT in buttons:
                    config = d.settings_menu(config_options)
                    os.system(config_dir + "/"+config)
            time.sleep(1.0/freq)
            animation_count = (animation_count + 1) % len(status_animation)
