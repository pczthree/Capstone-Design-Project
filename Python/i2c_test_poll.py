import smbus
from sys import stdout
import time
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x05

def writeNumber(value):
	bus.write_byte(address, value)
	return -1

def readNumber():
	number = bus.read_byte(address)
	return number

def readString():
	byte_in = 0
	byte_list = []
	for i in range(2):
		byte_list.append(bus.read_byte(address))

	return byte_list
	
def readArray():
	byte_in = 0
	byte_list = []
	for i in range(10):
		byte_list.append(bus.read_byte(address))

	return byte_list
while True:
	# number = readNumber()
	my_list = readArray()
	for i in range(len(my_list)):
		stdout.write(chr(my_list[i]))
	stdout.write('\n')
	time.sleep(1)
