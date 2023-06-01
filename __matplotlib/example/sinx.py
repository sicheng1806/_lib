import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker


fig,ax = plt.subplots()
ax.autoscale(False)
#
ax.set_xlim([-5*np.pi,5*np.pi])
ax.set_ylim([-2,2])
ax.spines["left"].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#
ax.xaxis.set_major_locator(mticker.MultipleLocator(base = np.pi))
ax.set_xticklabels(['${:d}\pi$'.format(int(i/np.pi)) for i in ax.get_xticks()])


x = np.arange(-10*np.pi,10*np.pi,0.01*np.pi)
y = np.sin(x)
ax.plot(x,y,color = 'blue')

plt.show()
