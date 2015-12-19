import RPi.GPIO as gpio
import time 

NUM_CYCLES = 5
CENTER = 1500
list_size = 10
pw_array = [CENTER for i in range(list_size)]

def measurePulseWidth(pin):
	"""Returns pulse width in seconds of a square wave on pin *pin*"""
	gpio.wait_for_edge(pin, gpio.RISING)
	start = time.time()
	gpio.wait_for_edge(pin, gpio.FALLING)
	pw = time.time() - start
	if(pw_avg > 2000):
		return 2000
	elif(pw_avg < 1000):
		return 1000
	else:
		return pw_avg

def measurePulseWidthMicro(pin):
	"""Returns pulse width in microseconds of a square wave on pin *pin*"""
	return 1000000*measurePulseWidth(pin)

# This function works with increasing frequency. If the frequency rises
# above 100 Hz then falls below, it multiplies by 10
def measurePWMFrequency(pin):
	""" Returns the frequency in Hz of a square wave on pin *pin*"""
	frequency = 0
	start = time.time()
	for impulse_count in range(NUM_CYCLES):
		gpio.wait_for_edge(pin, gpio.FALLING)
	duration = time.time() - start
	frequency = NUM_CYCLES / duration
	return frequency
