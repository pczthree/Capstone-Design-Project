from Adafruit_PWM_Servo_Driver import PWM
import csv
import FilterTools as ft
import numpy as np
import PWMTools as pwt 
import RPi.GPIO as gpio
import ServoTools as st
from sys import stdout
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)
print('PWM device initialized')

#=========================
# INITIALIZE FILTER	
#=========================
filter_order = 4
filter_freq = 0.4
filter_atten = 40

ic_input = np.zeros(filter_order) + 1500
ic_filter = np.zeros(filter_order) + 1500

cheby2 = ft.FilterTools(0, filter_order, filter_freq, 'low', filter_atten)

print('Filter initialized')

#=========================
# INITIALIZE INPUTS	
#=========================
aileron_in = 33 # BCM GPIO13

gpio.setmode(gpio.BOARD)
gpio.setup(aileron_in, gpio.IN)

print('Inputs initialized')

#=========================
# DEFINE TIMING VARIABLES
#=========================
freq = int(pwt.measure_freq(aileron_in))
stdout.write("\rFrequency (Hz): %d\n" %freq)
pulse_length = 1000000 / (freq * 4096)

print('Timing variables initialized')

#=========================
# INITIALIZE OUTPUTS	
#=========================
aileron_out = 0 # Servo driver board
aileron = st.ServoTools(aileron_out, freq)

print('Outputs initialized')

#=========================
# OPEN WRITE STREAM
#=========================
# File needs to be removed before execution
ofile = open('signal.csv','wb')
w = csv.writer(ofile, delimiter=',',quoting=csv.QUOTE_NONE)

print('Write stream initialized')

#=========================
# EXECUTE PROCESSES
#=========================
db = 50
try:
	while(True):
		pw = int(pwt.measure_pw_us(aileron_in))
		# aileron.set_pw(pw)

		aileron_filt = cheby2.rtfilter(pw, ic_input, ic_filter)
		pw_filt = aileron_filt['y']
		if(np.absolute(pw - pw_old) > db):
			# Change to pw for unfiltered process
			aileron.set_pw(pw_filt)
		# Below may need to be part of the deadband as well	
		ic_input = aileron_filt['ic_input']
		ic_filter = aileron_filt['ic_filter']
		pw_old = pw

		w.writerow([pw, pw_filt])
		stdout.write("\rPulse Width: %d" %pw)
		stdout.flush()

except KeyboardInterrupt:
	pass

aileron.reset()
ofile.close()
