from Adafruit_PWM_Servo_Driver import PWM
pwm = PWM(0x40)

class ServoTools(object):




	def __init__(self, channel, freq, neutral=1500):
		self.channel = channel
		self.freq = freq
		self.neutral = neutral
		
		pwm.setPWMFreq(freq)
		self.pulse_length = 1000000 / (freq * 4096)

	def reset(self):
		set_pw(self.channel, self.neutral)

	def set_pw(self, time): # in us
		num_pulses = int(time / self.pulse_length)
		pwm.setPWM(self.channel, 0, num_pulses)

	# Add calibration process using Michael's experiment