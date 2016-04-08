from Adafruit_PWM_Servo_Driver import PWM
import csv
import FilterTools as ft
import numpy as np
import PWMTools as pwt
import RPi.GPIO as gpio
import ControlTools as ct
from sys import stdout
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)
print('PWM device initialized')

#=========================
# INITIALIZE FILTER	
#=========================
filter_order = 2
filter_freq = 0.4
filter_atten = 20

ic_input = np.zeros(filter_order) + 1500
ic_filter = np.zeros(filter_order) + 1500

cheby2 = ft.FilterTools(0, filter_order, filter_freq, 'low', filter_atten)

print('Filter initialized')

#=========================
# INITIALIZE INPUTS	
#=========================
aileron_in = 33 # BCM GPIO13 35 is GPIO19   37 is GPIO26   38 is GPIO20
elevator_in = 35
motor_in = 38
rudder_in = 37


gpio.setmode(gpio.BOARD)
gpio.setup(aileron_in, gpio.IN)
gpio.setup(elevator_in, gpio.IN)
gpio.setup(motor_in, gpio.IN)
gpio.setup(rudder_in, gpio.IN)

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
aileron_out = 0 # Servo driver board on frequency calibrated earlier
elevator_out = 1
motor_out = 2
rudder_out = 3

aileron = ct.Servo(aileron_out, freq)
elevator = ct.Servo(elevator_out, freq)
motor = ct.ESC(motor_out, freq)
rudder = ct.Servo(rudder_out, freq)


print('Outputs initialized')

#=========================
# OPEN WRITE STREAM
#=========================
# File needs to be removed before execution
ofile = open('signal.csv','wb')
w = csv.writer(ofile, delimiter=',',quoting=csv.QUOTE_NONE)

print('Write stream initialized')
w.writerow([aileron, elevator, motor, rudder])

#=========================
# EXECUTE PROCESSES
#=========================
try:
	while(True):
		pw = int(pwt.measure_pw_us(aileron_in))
		# aileron.set_pw(pw)

		aileron_filt = cheby2.rtfilter(pw, ic_input, ic_filter)
		aileron.set_pw(aileron_filt['y'])
		ic_input = aileron_filt['ic_input']
		ic_filter = aileron_filt['ic_filter']

		w.writerow([pw, aileron_filt['y']])
		# w.writerow([pw])
		stdout.write("\rPulse Width: %d" %pw)
		stdout.flush()

except KeyboardInterrupt:
	pass

aileron.reset()
ofile.close()
