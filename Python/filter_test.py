import BinVectorTools as bvt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal as sig

Ns = 10
Rs = 10
sens = 0.05

figCount = 1

## Generate input vector and add noise
X = bvt.OversampleBinVector(bvt.GenerateBinVector(Ns, 0), Rs)
wgn = sens*np.random.randn(1, Ns*Rs)[0]
Xn = X + wgn

gca = plt.figure(figCount)
figCount += 1
plt.stem(X)
plt.axis([0, Ns*Rs, -0.5, 1.5])
gca.suptitle('Input Without Noise', fontsize = 18)

gca = plt.figure(figCount)
figCount += 1
plt.stem(Xn)
plt.axis([0, Ns*Rs, -0.5, 1.5])
gca.suptitle('Input With WGN', fontsize = 18)

## Generate filter coefficients
b, a = sig.cheby2(2, 20, 0.4, 'low', analog=False, output='ba')
Yc = sig.lfilter(b, a, X)
Ycn = sig.lfilter(b, a, Xn)

gca = plt.figure(figCount)
figCount += 1
plt.stem(Yc)
plt.axis([0, Ns*Rs, -0.5, 1.5])
gca.suptitle('Chebyshev II Output Without Noise', fontsize = 18)

gca = plt.figure(figCount)
figCount += 1
plt.stem(Ycn)
plt.axis([0, Ns*Rs, -0.5, 1.5])
gca.suptitle('Chebyshev II Output With WGN', fontsize = 18)

plt.show()