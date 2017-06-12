import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const

liste = ['a', 'c', 'd', 'e']
p0liste = [[3000, 50, 300, 220], [3000, 50, 400, 220], [3000, 50, 600, 220],
           [3000, 50, 750, 220]]

f = np.array((10.62e6, 20.56e6, 25e6, 29.423e6))


def cauchy(x, N, s, t, b):
    return -N/np.pi * (s/(s**2 + (x-t)**2))+b

def auswerten(param):
    name, p0 = param
    I1, U1 = np.genfromtxt('daten/'+name+'1.txt', unpack=True)
    I2, U2 = np.genfromtxt('daten/'+name+'2.txt', unpack=True)

    popt1, pcov1 = curve_fit(cauchy, I1, U1, maxfev=10000000, p0=p0)
    popt2, pcov2 = curve_fit(cauchy, I2, U2, maxfev=10000000, p0=p0)

    x = np.linspace(0, 900, 1000)

    plt.plot(x, cauchy(x, *popt1), 'C0')
    plt.plot(x, cauchy(x, *popt2), 'C1')
    plt.plot(I1, U1, 'x')
    plt.plot(I2, U2, 'x')
    plt.savefig('build/'+name+'.pdf')
    plt.close()
    return np.mean((popt1[2], popt2[2])), 0.5*np.abs((popt1[2]-popt2[2]))


I = np.array(list(map(auswerten, zip(liste, p0liste))))/1e3
Ig = I.T[0]
dI = I.T[1]

Bg = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * Ig
g = - const.h * f / (Bg * (0.5 * const.e / const.m_e * const.hbar))

dB = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * dI

print(g.mean())
print('{} µT'.format(dB.mean()*1e6))
