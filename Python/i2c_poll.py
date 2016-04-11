import smbus
from sys import stdout
import time
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x05

def writeNumber(value):
	bus.write_byte(address, value)
	return -1
	
def readString():
	bus.write_byte(address, 1)
	byte_in = 1
	byte_list = []
	while byte_in != 0:
		byte_in = bus.read_byte(address)
		time.sleep(0.005)
		byte_list.append(byte_in)
	return byte_list

while True:
	my_list = readString()
	del my_list[-1]
	for ii in range(len(my_list)):
		stdout.write(str(unichr(int(my_list[ii]))))
	stdout.write('\n')
	time.sleep(1)
