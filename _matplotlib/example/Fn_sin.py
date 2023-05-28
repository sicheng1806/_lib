from __functools import Fn
from _matplotlib import changeToMath
import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()
changeToMath(ax,[-4*np.pi,4*np.pi],[-2,2],1/2*np.pi,1/2)
ax.set_xticklabels(['${:.2}\pi$'.format(i/np.pi) for i in ax.get_xticks()])

x = np.linspace(-4*np.pi,4*np.pi,1000)
ys = [Fn(np.sin,n,x) for n in range(1,1000)]

for y in  ys:
    ax.plot(x,y)
ax.plot([-4*np.pi,4*np.pi],[1,1])
ax.plot([-4*np.pi,4*np.pi],[-1,-1])
plt.show()

