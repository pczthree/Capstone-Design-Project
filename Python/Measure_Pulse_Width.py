#!/usr/bin/env python

"""Measure_Pulse_Width.py: Determines the pulse width of a square wave input"""

from numpy import roll
import RPi.GPIO as gpio
from sys import stdout
import time 

NUM_CYCLES = 5
CENTER = 1500
list_size = 10
pw_array = [CENTER for i in range(list_size)]

def measurePulseWidthSec(pin):
	gpio.wait_for_edge(pin, gpio.RISING)
	start = time.time()
	gpio.wait_for_edge(pin, gpio.FALLING)
	pw = time.time() - start
	return pw

def measurePulseWidthMicro(pin):
	pw_avg = 0
	for i in range(NUM_CYCLES):
		gpio.wait_for_edge(pin, gpio.RISING)
		start = time.time()
		gpio.wait_for_edge(pin, gpio.FALLING)
		pw_avg = pw_avg + (time.time() - start)
	pw_avg = (pw_avg * 1000000) / NUM_CYCLES
	if(pw_avg > 2000):
		return 2000
	elif(pw_avg < 1000):
		return 1000
	else:
		return pw_avg

def measurePulseWidthMovingAverageSec(pin):
	global pw_array
	gpio.wait_for_edge(pin, gpio.RISING)
	start = time.time()
	gpio.wait_for_edge(pin, gpio.FALLING)
	pw_array[0] = time.time() - start
	pw_array = roll(pw_array, 1)
	pw_avg = sum(pw_array) / float(len(pw_array))
	if pw_avg > 0.002:
		return 0.002
	elif pw_avg < 0.001:
		return 0.001
	else:
		return pw_avg
