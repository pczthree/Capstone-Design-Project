import RPi.GPIO as gpio
import time

STATUS_LED = 37 # BOARD 37 = BCM 26

gpio.setmode(gpio.BOARD)
gpio.setup(STATUS_LED, gpio.OUT)

time.sleep(10)

gpio.output(STATUS_LED, 1)
