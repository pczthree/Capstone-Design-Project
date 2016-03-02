import FilterTools as ft
import BinVectorTools as bvt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

Ns = 10
Rs = 10
sens = 0.005

## Generate input vector and add noise
X = bvt.OversampleBinVector(bvt.GenerateBinVector(Ns, 0), Rs)
wgn = sens*np.random.randn(1, Ns*Rs)[0]
Xn = X + wgn

filt1 = ft.FilterTools(1, 3, 0.6, 'low')
Yc = filt1.filter(X)
Ycn = filt1.filter(Xn)

print filt1.rise_time()
print filt1.overshoot()
print filt1.rtfilter(7, np.arange(3)+1, np.arange(3)+2)
print filt1.get_coef()['b']
print filt1.get_coef()['a']

a = np.random.random(50)
af = filt1.filter(a)



print a
print af