#!/usr/bin/env python3

import quick2wire.i2c as i2c
import time
import datetime
import sys

adc_address1 = 0x68
adc_address2 = 0x69

varDivisior = 16 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

with i2c.I2CMaster() as bus:
	
	def changechannel(address, adcConfig):
		bus.transaction(i2c.writing_bytes(address, adcConfig))
		
	def getadcreading(address):
		h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
		t = h << 8 | m 
		# check if positive or negative number and invert if needed
		if (h > 128):
			t = ~(0x020000 - t)
		return t * varMultiplier

	def setadc(addr):
		mode = 1
		sr = 2   # 0:240, 1:60, 2:15, 3:3.75 
		gain = 0 # gain = 2^x
		
		config_register = 0;
		config_register |= 0    << 5
		config_register |= mode << 4
		config_register |= sr   << 2
		config_register |= gain

		bus.transaction(i2c.writing_bytes(addr, config_register))

	setadc(adc_address1)
	changechannel(adc_address2, 0x9C)
	old_sample = 5.0
	while True:	
		start = datetime.datetime.now()
		val1 = getadcreading(adc_address1)
		end = datetime.datetime.now()


		ns = (old_sample*4 + val1) / 5.0
		v1 = "%0.8f" % ns
		v2 = "%0.8f" % val1
		old_sample = ns
		
		sys.stdout.write( str(time.time()) + "\t" + v1 + "\t" + v2 + "\n")
		sys.stdout.flush()
		time.sleep(0.05)	
