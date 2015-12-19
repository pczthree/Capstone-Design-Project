#!/usr/bin/python

#=========================
# IMPORT MODULES
#=========================
from Adafruit_PWM_Servo_Driver import PWM
import Measure_Pulse_Width as mpw
import Measure_PWM_Frequency as mpf
import RPi.GPIO as gpio
from sys import stdout
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
# pwm = PWM(0x40, debug=True)

#=========================
# CHANNEL INITIALIZATION	
#=========================
CH1_IN = 33 # BCM GPIO13
CH1_OUT = 0

gpio.setmode(gpio.BOARD)
gpio.setup(CH1_IN, gpio.IN)

#=========================
# DEFINE TIMING VARIABLES
#=========================
CENTER = 1500
FREQUENCY = int(mpf.measurePWMFrequency(CH1_IN))
#FREQUENCY = 42
stdout.write("\rFrequency (Hz): %d\n" %FREQUENCY)
servoMin = 164  # Min pulse length out of 4096
servoMax = 328  # Max pulse length out of 4096
pulseLength = 1000000 / (FREQUENCY * 4096)

#=========================
# DEFINE FUNCTIONS
#=========================
def resetCenter(channel):
	setPulseWidth(channel, CENTER)

def setServoPulse(channel, pulse):
	pulseLength = 1000000	                 # 1,000,000 us per second
	period /= FREQUENCY		                     # in us
	#print "%d us per period" % pulseLength
	pulseLength = period / 4096                     # 12 bits of resolution
	#print "%d us per bit" % pulseLength
	pulse *= 1000
	pulse /= pulseLength
	pwm.setPWM(channel, 0, pulse)

def setPulseWidth(channel, time): # in us
	numPulses = int(time / pulseLength)
	pwm.setPWM(channel, 0, numPulses)

def shutdownAll(channel):
	setPulseWidth(channel, 1000)

#=========================
# EXECUTE PROCESSES
#=========================
pwm.setPWMFreq(FREQUENCY)                      # Set frequency to 60 Hz

try:
#	while (True):
#		# Change speed of continuous servo on channel O
#		pwm.setPWM(CH1_OUT, 0, servoMin)
#		time.sleep(1)
#		pwm.setPWM(CH1_OUT, 0, servoMax)
#		time.sleep(1)
	while(True):
		pw = int(mpw.measurePulseWidthMicro(CH1_IN))
#		pw = int(mpw.measurePulseWidthMovingAverageSec(CH1_IN) * 1000000)
		setPulseWidth(CH1_OUT, pw)
		stdout.write("\rPulse Width: %d" %pw)
		stdout.flush()

except KeyboardInterrupt:
	resetCenter(CH1_OUT)
