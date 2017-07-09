import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import uncertainties.unumpy as unp
import uncertainties as unc
import scipy.stats
from scipy.optimize import curve_fit
import tools

data = np.genfromtxt('daten/glas.txt', dtype=object, unpack=True)

theta = np.deg2rad(data[0].astype(float))
M = data[1:4].astype(float)
M = unp.uarray(M.mean(axis=0), M.std(axis=0)).cumsum()

tools.table((data[0], *data[1:4], M), (r'\phi/\degree', 'M_1', 'M_2', 'M_3', 'M'), 'build/glas.tex', 'Messdaten und Ergebnisse der Glasmessung.', 'tab:glas', round_figures=(0, 3, 0, 0, 0, 3))

T = 1e-3
lambda_ = 623.990e-9
alpha = np.deg2rad(10)


def func(theta, n):
    return T/lambda_ * (n-1)/(2*n) * ((alpha+theta)**2 - (alpha-theta)**2)

params, pcov = curve_fit(func, theta, unp.nominal_values(M))
print(unc.correlated_values(params, pcov))
theta_s = np.linspace(-1, 1, 1000)

plt.plot(1e3*theta_s, func(theta_s, *params), label='Fit')
plt.xlim(0, 0.2*1e3)
plt.ylim(0, 40)
#plt.yscale('log')
#plt.xscale('log')
plt.xlabel(r'$\theta/\mathrm{mrad}$')
plt.ylabel(r'$M$')
plt.errorbar(1e3*theta, unp.nominal_values(M), yerr=unp.std_devs(M), fmt='x', label='Messdaten')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/glas.pdf')
