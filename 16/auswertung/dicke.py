#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy.constants as const
import tools
import uncertainties as unc
import uncertainties.unumpy as unp

data1 = np.genfromtxt('daten/dicke_ohne.txt', unpack=True, dtype=object)
data2 = np.genfromtxt('daten/dicke_mit.txt', unpack=True, dtype=object)

tools.table([data1[0], data1[1], data2[0], data2[1]], ["U_1/V", "p_1/hPa", "U_2/V", "p_2/hPa"], "build/table_energieverlust.tex", "Messdaten der Energieverlustmessung", "tab:daten1", split=1, footer=None, round_figures=None, interrows=None)

U1, p1 = data1.astype(float)
U2, p2 = data2.astype(float)


slope1, intercept1, r_value, p_value, std_err1 = stats.linregress(p1, U1)
slope2, intercept2, r_value, p_value, std_err2 = stats.linregress(p2, U2)

mx = p1.mean()
sx2 = ((p1-mx)**2).sum()
intercept_err1 = std_err1 * np.sqrt(1./len(p1) + mx*mx/sx2)

mx = p2.mean()
sx2 = ((p2-mx)**2).sum()
intercept_err2 = std_err2 * np.sqrt(1./len(p2) + mx*mx/sx2)

intercept1 = unc.ufloat(intercept1, intercept_err1)
intercept2 = unc.ufloat(intercept2, intercept_err2)


x = np.linspace(0, 325)

plt.plot(x, slope1 * x + intercept1.n, 'C0', label='Fit ohne Folie')
plt.plot(x, slope2 * x + intercept2.n, 'C1', label='Fit mit Folie')

print('Pulshöhendifferenz: {}'.format(intercept1-intercept2))
print('Druckdifferenz: {}'.format(-intercept1/slope1 + intercept2/slope2))
plt.plot(p1, U1, 'x', label='Daten ohne Folie')
plt.plot(p2, U2, 'x', label='Daten mit Folie')

plt.xlabel(r'$p/\mathrm{hPa}$')
plt.ylabel(r'$U/\mathrm{V}$')
plt.xlim(0, 325)
plt.ylim(0, 9)
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/plot2.pdf')

z = 2
p = (+intercept2/slope2 - intercept1/slope1) * 100
T = 295
N = p / (const.k * T)
Z = 7
m = const.m_e
Ekin = 5.486e6 * const.e
#Ekin = 5.16e6 * const.e

E0 = 3727e6 * const.e
v = const.c * np.sqrt(1-(1/(1+Ekin/E0))**2)
i = 10 * const.e * Z
dx = 101e-3

de = 4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i) * dx

Z = 79
N = 97986 * const.N_A
i = 10 * const.e * Z
print(N)

#dx = de / (4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i))
#print('{}µm'.format(dx*1e6))

de = 5.486e6 * const.e * (1-intercept2/intercept1)
dx = de / (4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i))
print('{}µm'.format(dx*1e6))
