from Adafruit_PWM_Servo_Driver import PWM
import numpy as np
import PWMTools as pwt
import RPi.GPIO as gpio

class ControlSurface(object)

	def __init__(self, channel, freq):
		self.channel = channel
		self.freq = freq
		
		pwm.setPWMFreq(freq)
		self.pulse_length = 1000000 / (freq * 4096)

	def reset(self):
		set_pw(self.channel, self.neutral)

	def set_pw(self, time): # in us
		num_pulses = int(time / self.pulse_length)
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
		self.center = sum(c)/len(c)

class Servo(ControlSurface):
	def __init__(self, channel, freq, neutral=1500):
		super(Servo).__init__(self, channel, freq)
		self.neutral = neutral

class ESC(ControlSurface):
	def __init__(self, channel, freq, neutral=0):
		super(ESC).__init__(self, channel, freq)
		self.neutral = neutral