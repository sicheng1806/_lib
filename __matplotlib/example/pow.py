from _matplotlib import changeToMath
import numpy as np
import matplotlib.pyplot as plt

fig,ax = plt.subplots()
ax.set_title("$y = x^i$")

changeToMath(ax,xlim=[-10,10],ylim=[-10,10],xmajor_base=1,ymajor_base=1)

x = np.linspace(-10,10,1000)
ys = [np.power(x,i) for i in np.arange(-3,4,1)]
for y in ys:
    ax.plot(x,y)
plt.show()