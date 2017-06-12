import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats
import tools

# An den Leser: Das hier ist nicht besonders sinnvoll, wenn man den Versuch
# richtig durchgeführt hat.

liste = ['a', 'c', 'd', 'e']
p0liste = [[3000, 50, 300, 220], [3000, 50, 400, 220], [3000, 50, 600, 220],
           [3000, 50, 750, 220]]

f = np.array((10.62e6, 20.56e6, 25e6, 29.423e6, 15.9037e6))


def cauchy(x, N, s, t, b):
    return -N/np.pi * (s/(s**2 + (x-t)**2))+b

def auswerten(param):
    name, p0 = param
    I1, U1 = np.genfromtxt('daten/'+name+'1.txt', unpack=True)
    I2, U2 = np.genfromtxt('daten/'+name+'2.txt', unpack=True)

    popt1, pcov1 = curve_fit(cauchy, I1, U1, maxfev=10000000, p0=p0)
    popt2, pcov2 = curve_fit(cauchy, I2, U2, maxfev=10000000, p0=p0)

    x = np.linspace(0, 950, 1000)
    plt.xlim(0, 950)
    plt.xlabel(r'$I/\mathrm{mA}$')
    plt.ylabel(r'$U_B / \mathrm{mV}$')
    plt.plot(x, cauchy(x, *popt1), 'C0', label="Fit (mod. Cauchy/Lorentz)")
    plt.plot(x, cauchy(x, *popt2), 'C1', label="Fit (mod. Cauchy/Lorentz)")
    plt.plot(I1, U1, 'x', label='Daten 1')
    plt.plot(I2, U2, 'x', label='Daten 2')
    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/'+name+'.pdf')
    plt.close()
    return popt1[2], popt2[2]


I = np.array(list(map(auswerten, zip(liste, p0liste)))).T/1e3


tools.table((f[:-1]/1e6, I[0]*1e3, I[1]*1e3), ('f/MHz', 'I_1/mA', 'I_2/mA'), 'build/ergfit.tex', 'Ermittelte Extremstellen, entsprechen der Resonanzfeldstärke.', 'tab:ergfit')

data_kal = np.genfromtxt('daten/kal.txt', dtype=object).T
tools.table(data_kal, ('l/mm', 'I/mA'), 'build/kal.tex', 'Daten der XY-Schreiber-Kalibrierung.', 'tab:kal')
kal_l, kal_i = data_kal.astype(float)
m, n, r, p, std = scipy.stats.linregress(kal_l, kal_i)

x = np.linspace(0, 210)
plt.plot(kal_l, kal_i, 'x', label='Kalibrierung XY-Schreiber')
plt.plot(x, m * x + n, label='Lin. Regression')
plt.xlim(0, 210)
plt.xlabel(r'$l/\mathrm{mm}$')
plt.ylabel(r'$I/\mathrm{mA}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/kal.pdf')
plt.close()

l = np.array((124.5, 145))
I_xy = (m*l+n)[np.newaxis].T/1e3
print(I_xy.shape, I.shape)
I = np.concatenate((I, I_xy), axis=1)
print(I)

Ig = np.mean(I, axis=0)
dI = I[1]-I[0]

Bg = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * Ig
g = - const.h * f / (Bg * (0.5 * const.e / const.m_e * const.hbar))

dB = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * dI

tools.table((f/1e6, Bg*1e6, g, dB*1e6), ('f/MHz', r'B/\micro\tesla', 'g', r'B_\bigoplus/\micro\tesla'), 'build/ergg.tex', r'Berechnete Messergebnisse von $g$ und $B_\bigoplus$.', 'tab:ergg')

print(g.mean(), g.std(ddof=1))
print('{}+-{} µT'.format(dB.mean()*1e6, dB.std(ddof=1)*1e6))
