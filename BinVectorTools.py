import numpy as np

def GenerateBinVector( N, choice ):
	if(choice == 0):
		x = np.random.choice(2, N)
		return x
	elif(choice == 1):
		x = np.random.choice(2, N)
		for ii in range(N):
			if x[ii] < 1:
				x[ii] = -1
		return x
	else:
		return 

def OversampleBinVector( A, N ):
	B = np.zeros((N,), dtype=np.int)
	B += 1
	K = np.transpose(np.kron(A,B))
	return K