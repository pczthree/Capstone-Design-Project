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
	bus.write_byte(address, 1)
	byte_in = 1
	byte_list = []
	while byte_in != 0:
		byte_in = bus.read_byte(address)
		time.sleep(0.005)
		byte_list.append(byte_in)
	# for i in range(5):
		# byte_list.append(bus.read_byte(address))
	return byte_list

while True:
	# number = readNumber()
	my_list = readArray()
	del my_list[-1]
	# print('The list: ')
	# print(my_list)
	for ii in range(len(my_list)):
		stdout.write(str(unichr(int(my_list[ii]))))
	stdout.write('\n')
	time.sleep(1)
