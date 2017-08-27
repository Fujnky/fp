import numpy as np
import matplotlib.pyplot as plt

def plot(name):
    bla,bla,bla,t,U,bla = np.genfromtxt('daten/bauteil'+name+'.csv', unpack=True, delimiter=',')
    t*=1e6
    plt.plot(t, U)
    plt.xlim(t.min(), t.max())
    plt.xlabel(r'$t/\mathrm{µs}$')
    plt.ylabel(r'$U/\mathrm{V}$')
    plt.tight_layout(pad=0)
    plt.savefig('build/bauteil'+name+'.pdf')
    plt.close()

plot('3.5')
plot('3.7')
plot('3.10')
