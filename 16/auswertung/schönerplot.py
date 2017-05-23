#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import tools
import uncertainties.unumpy as unp

data = np.genfromtxt('daten/streuquerschnitt.txt', unpack=True, dtype=object)

theta, N, t = data.astype(float)

N0 = 5360/180
N = N/t
N = unp.uarray(N, np.sqrt(N))
F = 2e-3 * 10e-3
N_T = 2e-6 * F * 97986 * const.N_A

sigma = N/N0 * F/N_T
omega = (F / 101e-3**2)
print(omega)
difsigma = sigma / omega

tools.table([data[0], data[1], data[2], N, difsigma], [r'\theta/\degree', r'N_\text{mess}', 't/s', r'N/\per\second', r'\frac{\mathrm{d}\sigma}{\mathrm{d}\Omega}(\theta)/\mathrm{m}^2'], 'build/daten2.tex', 'Messwerte und daraus abgeleitete Größen bei der Messung des Streuquerschnitts.', 'tab:daten2', split=1)

plt.errorbar(theta, unp.nominal_values(difsigma), yerr=unp.std_devs(difsigma), fmt='x', label='Messwerte')
plt.xlabel(r'$\theta/^\circ$')
plt.ylabel(r'$\frac{\mathrm{d}\sigma}{\mathrm{d}\Omega}(\theta)/\mathrm{m}^2$')
plt.ylim(-0.1e-21, 2.6e-21)
plt.xlim(-5, 25)

theta_th = np.linspace(1.5, 27, 1000)
theosigma = 1/(4 * np.pi * const.epsilon_0) ** 2 * (2 * 79 * const.e ** 2 / (4 * 5.486e6 * const.e))**2 * 1 / (np.sin(theta_th / 360 * 2 * np.pi/2) ** 4)
plt.plot(theta_th, theosigma, '-', label='Theoriekurve')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/plot3.pdf')
