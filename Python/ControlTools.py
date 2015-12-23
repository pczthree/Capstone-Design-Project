from Adafruit_PWM_Servo_Driver import PWM
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

class Servo(ControlSurface):
	def __init__(self, channel, freq, neutral=1500):
		super(Servo).__init__(self, channel, freq)
		self.neutral = neutral

class ESC(ControlSurface):
	def __init__(self, channel, freq, neutral=1500):
		super(ESC).__init__(self, channel, freq)
		self.neutral = neutral