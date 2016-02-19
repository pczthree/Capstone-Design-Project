import numpy as np
from scipy import signal as sig

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

		return {'y':this_filter[self.filter_order-1], 'ic_input':this_input, 'ic_filter':this_filter}
