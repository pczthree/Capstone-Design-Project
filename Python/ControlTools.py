from Adafruit_PWM_Servo_Driver import PWM
import numpy as np
import PWMTools as pwt
import RPi.GPIO as gpio
import ServoTools as st

class ControlSurface(object):
	"""This class provides access to PWMTools with additional features for
	general control surface types. Contained within are functions to:
	Reset to neutral
	Set pulse width
	Calibrate range of motion
	"""

	def __init__(self, channel, freq):
		self.channel = channel
		self.freq = freq
		self.max = 2000
		self.min = 1000
		
		pwm.setPWMFreq(freq)
		self.pulse_length = 1000000/(freq*4096)

	def reset(self):
		set_pw(self.channel, self.neutral)

	def set_pw(self, time): # in us
		if time > self.max:
			time = self.max
		elif time < self.min:
			time = self.min
		num_pulses = int(time/self.pulse_length)
		pwm.setPWM(self.channel, 0, num_pulses)

	def calibrate_ROM(self):
		threshold = 50
		x_ = self.neutral

		#hold min
		m = []
		for ii in range (10):
			x = pwt.measure_pw_us(channel)
			# will usually throw away the first point
			if np.absolute(x - x_) > threshold:
				ii -= 1
			else:
				m.append(pwt.measure_pw_us(channel))
			x_ = x
		self.min = sum(m)/len(m)

		#hold max
		M = []
		for ii in range (10):
			x = pwt.measure_pw_us(channel)
			# will usually throw away the first point
			if np.absolute(x - x_) > threshold:
				ii -= 1
			else:
				M.append(pwt.measure_pw_us(channel))
			x_ = x
		self.max = sum(M)/len(M)

		c = []
		for ii in range (10):
			x = pwt.measure_pw_us(channel)
			# will usually throw away the first point
			if np.absolute(x - x_) > threshold:
				ii -= 1
			else:
				c.append(pwt.measure_pw_us(channel))
			x_ = x
		self.neutral = sum(c)/len(c)

class Servo(ControlSurface):
	"""This class defines the behavior of a 1-2 ms servo"""
	def __init__(self, channel, freq, neutral=1500, run=False):
		super(Servo).__init__(self, channel, freq)
		self.neutral = neutral
		
		if run:
			self.main()

	def main(self):
		# update loop goes here
		pass

class ESC(ControlSurface):
	"""This class defines the behavior of a 1-2 ms AC motor electronic speed
	controller
	"""
	def __init__(self, channel, freq, neutral=1000, run=False):
		super(ESC).__init__(self, channel, freq)
		self.neutral = neutral

		if run:
			self.main()

	def main(self):
		# update loop goes here
		pass
