import RPi.GPIO as gpio
import time
import os

gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.IN)
while True:
   if(gpio.input(7)):
      os.system("sudo shutdown -h now")
   break
time.sleep(1)
