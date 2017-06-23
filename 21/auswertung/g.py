import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

f, I11, I12, I21, I22 = np.genfromtxt('daten/daten.txt', unpack=True)

f*=1e6

def helmholtz(I, N, r):
    return 8/np.sqrt(125) * const.mu_0 * N * I / r

B1 = helmholtz(I11, 11, 16.39e-2) + helmholtz(I12, 154, 15.79e-2)
B2 = helmholtz(I21, 11, 16.39e-2) + helmholtz(I22, 154, 15.79e-2)

g1 = const.h * f / (B1 * const.value('Bohr magneton'))
g2 = const.h * f / (B2 * const.value('Bohr magneton'))

print(const.value('Bohr magneton'))
print(g1.mean())
print(g2.mean())

plt.plot(f/1e6, B1*1e6, 'x')
plt.plot(f/1e6, B2*1e6, 'x')
plt.show()
