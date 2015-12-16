import numpy as np

def movingAverage( vals, window ):
	weights = np.repeat(1.0, window)/window
	sma = np.convolve(vals, weights, 'valid')
	return sma