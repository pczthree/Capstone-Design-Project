import BinVectorTools as bvt
import time
import FilterTools as ft
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal as sig
from scipy.interpolate import spline

def test_PID(P=1, I=0, D=0, n=1000):
	figCount = 1
	Ns = n
	Ts = 0.001
	## Generate input vector and add noise
	X = []
	for i in range(Ns):
		if i < 10:
			X.append(0)
		else:
			X.append(1)
	
	## Generate P controller with unit Kp
	p = ft.PID(P, I, D)
	p.setPoint(0)
	p.setSampleTime(Ts)
	feedback = 0
	
	## Filter X to generate Y
	Y = []
	t = range(Ns)
	setpoint_list = []
	
	for i in range(1, Ns):
		p.setPoint(X[i])
		p.update(feedback)
		output = p.output
		if p.SetPoint > 0:
		    feedback += (output - (1/i))
		time.sleep(1.1*Ts)
	
		Y.append(feedback)
		setpoint_list.append(p.SetPoint)
		#time_list.append(i)

	Y.insert(0, 0)
	gca = plt.figure(figCount)
	figCount += 1
	plt.plot(t, X, label='Step input')
	plt.plot(t, Y, 'k--', label='PID output')
	plt.axis([0, Ns, -0.5, 1.5])
	gca.suptitle('PID Test', fontsize = 18)
	plt.grid(True)
	plt.show()

if __name__ == "__main__":
	test_PID(n=100)