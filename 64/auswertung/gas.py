import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import uncertainties.unumpy as unp
import scipy.stats
import tools


data = np.genfromtxt('daten/gas.txt', dtype=object, unpack=True)


p = data[0].astype(float) * 100
M = data[1:4].astype(float)
M = unp.uarray(M.mean(axis=0), M.std(axis=0))

tools.table((*data, M), ('p/hPa', 'M_1', 'M_2', 'M_3', 'M'), 'build/gas.tex', 'Messdaten der Luftmessung.', 'tab:gas')

slope, intercept, bla, bla, bla = scipy.stats.linregress(p, unp.nominal_values(M))
p_norm = 101325
lambda_ = 623.990e-9
L = unp.uarray(100e-3, 0.1e-3)

M_norm = slope * p_norm + intercept
print(M_norm)

n = M_norm * lambda_ / (2*L) + 1
print(n)

p_=np.linspace(0, 1050*100)

plt.xlim(0, 1050)
plt.ylim(0, 45)
#plt.yscale('log')
#plt.xscale('log')
plt.xlabel(r'$p/\mathrm{hPa}$')
plt.ylabel(r'$M$')
plt.plot(p_/100, p_*slope + intercept, label='Lineare Regression')
plt.errorbar(p/100, unp.nominal_values(M), yerr=unp.std_devs(M), fmt='x', label='Messdaten')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/gas.pdf')
