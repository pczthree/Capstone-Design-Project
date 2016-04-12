import sys
import posix_ipc
import mmap

SHM_NAME = "/AVIONICS"
SEM_NAME = "/AVIONICS"

# configure shared memory and semaphore
shm_size = 1024
memory = posix_ipc.SharedMemory( SHM_NAME, 
                                 posix_ipc.O_CREAT, 
                                 size=shm_size )
sem = posix_ipc.Semaphore( SEM_NAME, posix_ipc.O_CREAT, initial_value = 1 )
mapfile = mmap.mmap(memory.fd, memory.size)
memory.close_fd()


def write_shm( msg ):
	mapfile.seek(0)
	mapfile.write(msg)
	mapfile.write('\0')

def read_shm():
	mapfile.seek(0)
	s = []
	c = mapfile.read_byte()
	while c != '\0':
		s.append(c)
		c = mapfile.read_byte()
	s = ''.join(s)
	return s


with posix_ipc.Semaphore(SEM_NAME) as sem:
	write_shm( str(sys.argv[1]) )


