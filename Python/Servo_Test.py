from Adafruit_PWM_Servo_Driver import PWM
import FilterTools as ft
import PWMTools as pwt 
import RPi.GPIO as gpio
import ServoTools as st
from sys import stdout
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)

#=========================
# INITIALIZE FILTER	
#=========================
filter_order = 4
filter_freq = 0.4
filter_atten = 40

ic_input = np.zeros(filter_order) + 1500
ic_filter = np.zeros(filter_order) + 1500

cheby2 = ft.FilterTools(0, filter_order, filter_freq, 'low', filter_atten)

#=========================
# INITIALIZE INPUTS	
#=========================
aileron_in = 33 # BCM GPIO13

gpio.setmode(gpio.BOARD)
gpio.setup(aileron_in, gpio.IN)

#=========================
# DEFINE TIMING VARIABLES
#=========================
freq = int(pwt.measure_freq(aileron_in))
stdout.write("\rFrequency (Hz): %d\n" %freq)
pulse_length = 1000000 / (FREQUENCY * 4096)

#=========================
# INITIALIZE OUTPUTS	
#=========================
aileron_out = 0 # Servo driver board
aileron = st.ServoTools(aileron_out, freq)

#=========================
# OPEN WRITE STREAM
#=========================
try:
	os.remove('signal.csv')
except WindowsError:
	pass

ofile = open('signal.csv','wb')
w = csv.writer(ofile, delimiter=',',quoting=csv.QUOTE_NONE)

#=========================
# EXECUTE PROCESSES
#=========================
try:
	while(True):
<<<<<<< HEAD
		pw = int(mpw.measure_pw_us(CH1_IN))
		# aileron.set_pw(pw)

		aileron_filt = cheby2.rtfilter(pw, ic_input, ic_filter)
		aileron.set_pw(aileron_filt['y'])
		ic_input = aileron_filt['ic_input']
		ic_filter = aileron_filt['ic_filter']

		w.writerow([pw, aileron_filt['y']])
=======
		pw = int(mpw.measure_pw_us(aileron_in))
		aileron.set_pw(pw)
>>>>>>> master
		stdout.write("\rPulse Width: %d" %pw)
		stdout.flush()

except KeyboardInterrupt:
	break

<<<<<<< HEAD
aileron.reset()
ofile.close()
=======
aileron.reset()
>>>>>>> master
