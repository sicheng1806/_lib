from _matplotlib import changeToMath
import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()
ax.set_title('cycloid')
changeToMath(ax,[0,10*np.pi],[-5,5],np.pi,1)
ax.set_xticklabels(["${:d}\pi$".format(int(i/np.pi)) for i in ax.get_xticks()])

t = np.linspace(0,10*np.pi,1000)
x = t - np.sin(t)
y = 1 - np.cos(t)

ax.plot(x,y)

plt.show()