#!/usr/bin/env python

"""Measure_PWM_Frequency.py: Determines the frequency of a square wave input"""

import RPi.GPIO as gpio
from sys import stdout
import time 

NUM_CYCLES = 100

""" This function works with increasing frequency. If the frequency rises above 100 Hz then falls below, it multiplies by 10 """
def measurePWMFrequency(pin):
	frequency = 0
	start = time.time()
	for impulse_count in range(NUM_CYCLES):
		gpio.wait_for_edge(pin, gpio.FALLING)
	duration = time.time() - start
	frequency = NUM_CYCLES / duration
	return frequency
