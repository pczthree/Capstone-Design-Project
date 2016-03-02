import numpy as np
from scipy import signal as sig
import time

class FilterTools(object):
	"""This class allows the user to generate Chebychev II or Butterworth
	filter coefficients and perform analysis and application. Contained within
	are functions to:
	Access coefficients
	Apply filter to an array
	Perform a discrete step response
	Determine rise time
	Determine overshoot
	Filter in real time
	"""

	def __init__(self, filter_type, filter_order, filter_freq,
			filter_direction, filter_atten=0):
		"""Return a FilterTools object of type *filter_type* as 0 == cheby2 or
		1 == butter of order *filter_order* with minimum attenuation
		*filter_atten* (for cheby2). *filter_freq* is the normalized cutoff
		frequency 2*fc/fs and *filter_direction* a string determining 'high'
		or 'low' pass behavior.
		"""
		# Handle exceptions
		# http://stackoverflow.com/questions/2525845/proper-way-
		#	in-python-to-raise-errors-while-setting-variables

		if(filter_type==0):
			self.b, self.a = sig.cheby2(filter_order, filter_atten,
					filter_freq, filter_direction, analog=False,
					output='ba')
		elif(filter_type==1):
			self.b, self.a = sig.butter(filter_order, filter_freq,
					filter_direction, analog=False,
					output='ba')

		self.filter_order = filter_order

	def get_coef(self):
		"""Return a dictionary of filter coefficients"""
		return {'b':self.b, 'a':self.a}

	def filter(self, X):
		"""Return result of applying filter coefficients to input X"""
		return sig.lfilter(self.b, self.a, X)

	def step(self, dt=1):
		"""Return discrete step response of filter"""
		return sig.dstep((self.b, self.a, dt))

	def rise_time(self):
		"""Return 90 percent rise time of step response in terms of samples"""
		s = sig.dstep((self.b, self.a, 1))[1][0]
		n = 0
		for ii in range(len(s)):
			if s[ii] > 0.9:
				n = ii
				break
		return n

	def overshoot(self):
		"""Return overshoot as decimal"""
		s = sig.dstep((self.b, self.a, 1))[1][0]
		m = max(s)
		return round(float(m - 1), 3)

	def rtfilter(self, new_input, ic_input=None, ic_filter=None):
		"""Generates and applies IIR filter to an input
		   Returns current output and sufficient past outputs to perform
		   future filtering
		"""

		if(ic_input==None):
			ic_input = np.zeros(self.filter_order)
		else:
			if(len(ic_input) != self.filter_order):
				raise IndexError(
					"initial input conditions must be sufficient for filter order")

		if(ic_filter==None):
			ic_filter = np.zeros(self.filter_order)
		else:
			if(len(ic_filter) != self.filter_order):
				raise IndexError(
					"initial output conditions must be sufficient for filter order")

		this_input = np.roll(ic_input, -1)
		this_input[self.filter_order-1] = new_input

		this_filter = np.roll(ic_filter, -1)

		ff = np.zeros(self.filter_order+1)
		fb = np.zeros(self.filter_order+1)
		ff[0] = self.b[0]
		fb[0] = self.a[0]
		for ii in range(1,self.filter_order+1):
			ff[ii] = self.b[ii]*this_input[ii-1]
			fb[ii] = self.a[ii]*this_filter[ii-1]
		y = sum(ff) - sum(fb)

		this_filter[self.filter_order-1] = y

		return {'y':this_filter[self.filter_order-1], 'ic_input':this_input,
				'ic_filter':this_filter}

class PID:
	"""This class provides a mechanism to implement PID control on an input
	   with reference to a set point. Contained within are accessors and
	   mutators for the set point, integral, and derivative terms, as well as
	   an accessor for the error term.
	"""
	# https://github.com/ivmech/ivPID

	def __init__(self, P=1, I=0.0, D=0.0):
		self.Kp = P
		self.Ki = I
		self.Kd = D

		self.sample_time = 0.00
		self.current_time = time.time()
		self.last_time = self.current_time

		self.clear()

	def clear(self):
		"""Clears PID computations and coefficients"""
		self.SetPoint = 0.0

		self.PTerm = 0.0
		self.ITerm = 0.0
		self.DTerm = 0.0
		self.last_error = 0.0

		# Windup Guard
		self.int_error = 0.0
		self.windup_guard = 20.0

		self.output = 0.0

	def update(self, feedback_value):
		"""Calculates PID value for given reference feedback
		.. math::
		    u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
		.. figure:: images/pid_1.png
		   :align:   center
		   Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
		"""
		error = self.SetPoint - feedback_value

		self.current_time = time.time()
		delta_time = self.current_time - self.last_time
		delta_error = error - self.last_error

		if (delta_time >= self.sample_time):
			self.PTerm = self.Kp * error
			self.ITerm += error * delta_time

			if (self.ITerm < -self.windup_guard):
				self.ITerm = -self.windup_guard
			elif (self.ITerm > self.windup_guard):
				self.ITerm = self.windup_guard

			self.DTerm = 0.0
			if delta_time > 0:
				self.DTerm = delta_error / delta_time

			# Remember last time and last error for next calculation
			self.last_time = self.current_time
			self.last_error = error

			self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

	def setKp(self, proportional_gain):
		"""Determines how aggressively the PID reacts to the current error
		with setting Proportional Gain"""
		self.Kp = proportional_gain

	def setKi(self, integral_gain):
		"""Determines how aggressively the PID reacts to the current error
		with setting Integral Gain"""
		self.Ki = integral_gain

	def setKd(self, derivative_gain):
		"""Determines how aggressively the PID reacts to the current error
		with setting Derivative Gain"""
		self.Kd = derivative_gain

	def setPoint(self, set_point):
		self.SetPoint = set_point

	def setWindup(self, windup):
		"""Integral windup, also known as integrator windup or reset windup,
		refers to the situation in a PID feedback controller where
		a large change in setpoint occurs (say a positive change)
		and the integral terms accumulates a significant error
		during the rise (windup), thus overshooting and continuing
		to increase as this accumulated error is unwound
		(offset by errors in the other direction).
		The specific problem is the excess overshooting.
		"""
		self.windup_guard = windup

	def setSampleTime(self, sample_time):
		"""PID that should be updated at a regular interval.
		Based on a pre-determined sampe time, the PID decides if it should
		compute or return immediately.
		"""
		self.sample_time = sample_time