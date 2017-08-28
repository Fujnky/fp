import numpy as np
import matplotlib.pyplot as plt
import peakdetect as peak
import tools

bla,bla,bla,f1,u1,bla = np.genfromtxt('daten/alpha_lang.csv', unpack=True, delimiter=',')
bla,bla,bla,f2,u2,bla = np.genfromtxt('daten/alpha_kurz.csv', unpack=True, delimiter=',')


p1 = peak.peakdetect(u1, f1, 1)
p2 = peak.peakdetect(u2, f2, 3)

plt.plot(f1/1e6, u1, '-', label='FFT des Signals auf Leitung 1')
plt.plot(f2/1e6, u2, '-', label='FFT des Signals auf Leitung 2')


p1 = np.array(p1[0]).T
p2 = np.array(p2[0]).T

p1 = p1.T[np.ma.mask_or(p1[1] > -15, np.logical_and(p1[0] > 1.1050e7, p1[0] < 1.1075e7))].T
p2 = p2.T[p2[1] > -15].T


plt.plot(p1[0]/1e6, p1[1], 'C0x', label='Peaks Leitung 1')
plt.plot(p2[0]/1e6, p2[1], 'C1x', label='Peaks Leitung 2')

alpha = p2[1]-p1[1]
tools.table((p1[0]/1e6, alpha), (r'f/MHz', r'\alpha/\deci\bel'), 'build/alpha.tex', 'Ergebnisse der Dämpfungsmessung.', 'tab:alpha', round_figures=(4,2), split=2)

print(alpha.mean(), alpha.std())

plt.ylabel(r'$L_P/\mathrm{dB}$')
plt.xlabel(r'$f/\mathrm{MHz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/alpha.pdf')
