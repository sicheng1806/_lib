import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker


def changeToMath(ax:plt.Axes,xlim:list[float],ylim:list[float],xmajor_base:float = None,ymajor_base = None):
    '''
    xlim = [-5,5],
    
    ylim = [-5,5],
    
    major_base = 2'''
    ax.autoscale(False)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.spines["left"].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    if xmajor_base:
        ax.xaxis.set_major_locator(mticker.MultipleLocator(base = xmajor_base))
    if ymajor_base:
            ax.yaxis.set_major_locator(mticker.MultipleLocator(base = ymajor_base))
    ax.text(xlim[1]+2,-3,'x').set_fontsize("x-large")
    ax.text(0,ylim[-1]+2,'y').set_fontsize("x-large")


if __name__ == '__main__':
    fig,ax = plt.subplots()
    changeToMath(ax,[-10*np.pi,10*np.pi],[-20,20],np.pi)
    ax.set_xticklabels(['${:d}\pi$'.format(int(i/np.pi)) for i in ax.get_xticks()])
    x = np.linspace(-6*np.pi,6*np.pi,100)
    ys = [x - np.sin(x)*a for a in np.linspace(0,1,10)]
    for y in ys:
        ax.plot(x,y,color = 'blue')
    plt.show()
