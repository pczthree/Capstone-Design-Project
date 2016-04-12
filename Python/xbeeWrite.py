import sys
import signal
import time
import serial
import RPi.GPIO as GPIO
import posix_ipc
import mmap

# The pi gpio pin tied to the xbee CTS
CTS_PORT = 3
SEM_NAME = "/AVIONICS"
SHM_NAME = "/AVIONICS"

#
# Use Raspberry PI GPIO packege to monitor the xbee CTS pin for transmit flow control
#
# Example code can be found here:
#     https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
#
# Set the GPIO as an input
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CTS_PORT, GPIO.IN)

#
# Use the pyserial package to write to serial port. 
#
# Documentation can be found here:
#     http://pythonhosted.org/pyserial/
#
# Configure the serial port. The USB serial cable shows up as /dev/ttyUSB0 when plugged
# into the raspberry pi USB controler
ser = serial.Serial(
#    port='/dev/ttyUSB0',
    port='/dev/console',
#    baudrate=115200,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#
# Set up a chunck of shared memory where data will be read from. Use the posix_ipc package
# to handle the shared memory. 
#
# Documentation can be found here:
#     http://semanchuk.com/philip/posix_ipc/
#
# The library will handle access to the shared memory but it can also be accessed from the
# command line by "cat /dev/shm/AVIONICS"
#  
# Configure shared memory
shm_size = 1024
memory = posix_ipc.SharedMemory( SHM_NAME, 
                                 posix_ipc.O_CREAT, 
                                 size=shm_size )

# Add a semaphore to guard access the the shared memory
sem = posix_ipc.Semaphore( SEM_NAME, posix_ipc.O_CREAT, initial_value = 1 )

# memory map the shared memory then close the file handle.
mapfile = mmap.mmap(memory.fd, memory.size)
memory.close_fd()


#
# write_shm
#    Write a message to the shared memory. This function seeks to the
#    begining of the memory segment then writes the message. A null
#    character is appended to indicate the end of the message
#
#    A caller should hold the semaphore before calling this function.
#
def write_shm( msg ):
	mapfile.seek(0)
	mapfile.write(msg)
	mapfile.write('\0')

#
# read_shm
#    Read the shared memory and return it as a string. The memory is read up to the
#    first null character. 
#
#    A caller should hold the semaphore before calling this function.
#
def read_shm():
	mapfile.seek(0)
	s = []
	c = mapfile.read_byte()
	while c != '\0':
		s.append(c)
		c = mapfile.read_byte()
	s = ''.join(s)
	return s

#
# Initialize some data to the shared memory. 
#
with posix_ipc.Semaphore(SEM_NAME) as sem:
	write_shm( "Initial Data" )



#
# Blocking send message
#
# Send a message out the serial port. Send at most 16 bytes at a time.
# Monitor the CTS pin to make sure we do not overrun the xbee tx buffer
#
def send_message_blk( msg ):
	i = 0
	while (i<len(msg)):
		# Check gpio to make sure there is 16 bytes in tx buffer
		# if gpio not ready wait for it
		if ( not(GPIO.input(CTS_PORT)) ):
			sys.stdout.write( 'x' )
			sys.stdout.flush()
		while ( not(GPIO.input(CTS_PORT)) ):
			time.sleep(.01)

		# write at most 16 bytes
		written = ser.write(msg[i:i+16])
		ser.flush()
		i+=written



print 'Sending packets: \n'
time_bucket = time.clock()
byte_bucket = 0

while 1:
	sys.stdout.write( '.' )
	sys.stdout.flush()

	#
	# Get the semaphore then read the shared memory
	#
	with posix_ipc.Semaphore(SEM_NAME) as sem:
		msg = read_shm()

	#
	# Send what was in the shared memory out the serial port
	#
	send_message_blk(msg)


	#
	# Do some calculating to print out some throughput numbers
	#
	now = time.clock()
	byte_bucket += 16

	# print throughput every 5 seconds
	if ( now - time_bucket > 5 ):
		rate = byte_bucket / (now - time_bucket)
		print "\n", time.asctime(), " - ", \
			"Bytes[", byte_bucket, "] ", \
			"Seconds[", now - time_bucket, "] ", \
			"Throughput[", rate, "] Bytes/Sec"
		byte_bucket = 0
		time_bucket = time.clock()

ser.close()


