#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy.constants as const


U1, p1 = np.genfromtxt('daten/dicke_ohne.txt', unpack=True)
U2, p2 = np.genfromtxt('daten/dicke_mit.txt', unpack=True)

slope1, intercept1, r_value, p_value, std_err1 = stats.linregress(p1, U1)
slope2, intercept2, r_value, p_value, std_err2 = stats.linregress(p2, U2)

x = np.linspace(0, 325)

plt.plot(x, slope1 * x + intercept1)
plt.plot(x, slope2 * x + intercept2)

print('Pulshöhendifferenz: {}'.format(intercept2-intercept1))
print('Druckdifferenz: {}'.format(-intercept2/slope2 + intercept1/slope1))
plt.plot(p1, U1, 'x')
plt.plot(p2, U2, 'x')

plt.xlabel(r'$p/\mathrm{hPa}$')
plt.ylabel(r'$U/\mathrm{V}$')
plt.xlim(0, 325)
plt.ylim(0, 9)
plt.tight_layout(pad=0)
plt.savefig('build/plot2.pdf')

z = 2
p = (-intercept2/slope2 + intercept1/slope1) * 100
T = 295
N = p / (const.k * T)
Z = 7
m = const.m_e
Ekin = 5.486e6 * const.e
E0 = 3727e6 * const.e
v = const.c * np.sqrt(1-(1/(1+Ekin/E0))**2)
i = 10 * const.e * Z
dx = 101e-3

de = 4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i) * dx

Z = 79
N = 97986 * const.N_A
i = 10 * const.e * Z

dx = de / (4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i))
print(dx)

de = 5.486e6 * const.e / intercept1 * (intercept2-intercept1)
dx = de / (4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i))
print(dx)
