import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import tools

data = np.genfromtxt('daten/kontrast.txt', dtype=object, unpack=True)
phi, Umin, Umax = data.astype(float)

phi = np.deg2rad(phi)

def f(x, A, phi, omega):
    return A * np.abs(np.sin(omega * x + phi))

 
K = (Umax-Umin)/(Umax+Umin)

tools.table((*data, K), (r'\phi/\degree', r'U_\mathrm{min}/\milli\volt', r'U_\mathrm{max}/\milli\volt', 'K'), 'build/kontrast.tex', 'Messdaten und Ergebnisse der Kontrastmessung.', 'tab:kontrast', round_figures=(None, None, None, 3))

params, pcov = scipy.optimize.curve_fit(f, phi, K, p0=[0.5,0,2])
A, phi_, omega = params
print(A)
print(np.rad2deg((np.pi*0.5 - phi_)/omega))
x = np.linspace(-0.4, 3.5, 2000)
plt.xlim(-0.4, 3.5)

plt.plot(x, f(x, *params), label='Fit')
plt.plot(phi, K, 'x', label='Messdaten')
plt.xlabel(r'$\phi/\mathrm{rad}$')
plt.ylabel(r'$K$')
plt.legend(loc='upper right')
plt.tight_layout(pad=0)
plt.savefig('build/kontrast.pdf')
