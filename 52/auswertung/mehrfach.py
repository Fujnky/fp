import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec

def plot(name):
    bla,bla,bla,t,U,bla = np.genfromtxt('daten/mehrfach'+name+'.csv', unpack=True, delimiter=',')
    t*=1e6
    t+=0.13

    #gs = matplotlib.gridspec.GridSpec(2, 1, height_ratios=[3,1])
    #plt = plt.subplot(gs[0])
    plt.plot(t, U, label='Gemessener Signalverlauf')
    plt.xlim(t.min(), t.max())
    plt.xlabel(r'$t/\mathrm{µs}$')
    plt.ylabel(r'$U/\mathrm{V}$')
    #plt.setp(ax1.get_xticklabels(), visible=False)

    #ax2 = plt.subplot(gs[1], sharex=ax1)
    x = (-0.1, 0,   0, 0.11, 0.11, 0.15, 0.15, 0.205, 0.205, 0.5)
    y = (-62,  -62, 2, 2,    7,    7,    13,   13,    69,    69)
    plt.plot(x, y, 'C1', label='Konstruierter Signalverlauf')
    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/mehrfach'+name+'.pdf')
    plt.close()

plot('1')

print('reflexionsfaktoren')
print(5/64)
print(6/5)
print(56/64)
