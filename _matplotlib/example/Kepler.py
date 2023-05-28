from _matplotlib import changeToMath
import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()
changeToMath(ax,[-10*np.pi,10*np.pi],[-20,20],np.pi)
ax.set_xticklabels(['${:d}\pi$'.format(int(i/np.pi)) for i in ax.get_xticks()])
x = np.linspace(-6*np.pi,6*np.pi,100)
ys = [x - np.sin(x)*a for a in np.linspace(0,1,10)]
for y in ys:
    ax.plot(x,y,color = 'blue')
plt.show()
