import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

phi, Umin, Umax = np.genfromtxt('daten/kontrast.txt', unpack=True)

phi = np.deg2rad(phi)

def f(x, A, phi, omega):
    return A * np.abs(np.sin(omega * x + phi))


K = (Umax-Umin)/(Umax+Umin)

params, pcov = scipy.optimize.curve_fit(f, phi, K, p0=[0.5,0,2])
A, phi_, omega = params
print(A)
print(np.rad2deg((np.pi*0.5 - phi_)/omega))
x = np.linspace(-0.2, 3.5, 2000)

plt.plot(x, f(x, *params))
plt.plot(phi, K, 'x')
plt.show()
