from __functools import Fn
from _matplotlib import changeToMath
import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()
changeToMath(ax,[-np.pi,np.pi],[-2,2],1/2*np.pi,1/2)
ax.set_xticklabels(['${:.2}\pi$'.format(i/np.pi) for i in ax.get_xticks()])

x = np.linspace(-1/2*np.pi,1/2*np.pi,10000)
ys = [Fn(np.tan,n,x) for n in range(1,50)]

for y in  ys:
    ax.scatter(x,y,s = 1)
plt.show()

