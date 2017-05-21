import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

z = 2
p = np.linspace(0, 1000e2, 1000)
T = 295
N = p / (const.k * T)
Z = 7
m = const.m_e
Ekin = 5.486e6 * const.e
E0 = 3727e6 * const.e
v = const.c * np.sqrt(1-(1/(1+Ekin/E0))**2)
i = 10 * const.e * Z

dedx = 4 * np.pi * const.e**4 * z**2 * N * Z / (m * v**2 * (4 * np.pi * const.epsilon_0)**2) * np.log(2 * m * v**2 / i)

plt.plot(p/100, dedx/const.e / 100 / 1e6, 'k')
plt.xlim(0, 1000)
plt.ylim(0, 0.5)
plt.xlabel('p/hPa')
plt.ylabel(r'$\frac{\Delta E}{\Delta x} / \frac{\mathrm{MeV}}{\mathrm{cm}}$')
plt.savefig('build/plot1.pdf')
