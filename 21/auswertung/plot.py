# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

a, b, c, t1, I1, z = np.genfromtxt('daten/I1.csv', unpack=True, delimiter=',')
a, b, c, t2, I2, z = np.genfromtxt('daten/I2.csv', unpack=True, delimiter=',')
a, b, c, t3, U3, z = np.genfromtxt('daten/U1.csv', unpack=True, delimiter=',')
a, b, c, t4, U4, z = np.genfromtxt('daten/U2.csv', unpack=True, delimiter=',')
a, b, c, t5, U5, z = np.genfromtxt('daten/U3.csv', unpack=True, delimiter=',')


def cauchy(x, N, s, t, b):
    return -N/np.pi * (s/(s**2 + (x-t)**2))+b


t = (t2+1.1)

lims = [[650+20, 800-30], [1180-30, 1290+40], [1430-30, 1550+30]]



ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5)
plt.plot(t, U5, 'x', markersize=2, label='Messdaten')
plt.setp(ax1.get_xticklabels(), visible=False)
plt.ylabel('Intensität/a.u.')


plateau = U5[1700:1800].mean()
print('Plateau: {}'.format(plateau))

print('Minima:')
i = 1
for lim in lims:
    t_sl = t[lim[0]:lim[1]]
    U_sl = U5[lim[0]:lim[1]]
    params, pcov = scipy.optimize.curve_fit(cauchy, t_sl, U_sl, maxfev=1000000)

    t_syn = np.linspace(t[lim[0]], t[lim[1]], 1000)
    plt.plot(t_syn, cauchy(t_syn, *params), label='Fit {}'.format(i))

    print(params[2], plateau-cauchy(params[2], *params))
    i+=1


plt.legend(loc='best')

# share x only
ax2 = plt.subplot2grid((6, 1), (5, 0), sharex=ax1)
# make these tick labels invisible
plt.ylabel(r'$I/\mathrm{A}$')
plt.plot(t, (I2+142)/278  , 'x', markersize=1)
plt.xlabel(r'$t/\mathrm{s}$')
plt.setp(ax2.get_xticklabels())
plt.xlim(-0.05, 2.05)

plt.tight_layout(pad=0)
plt.savefig('build/plot2.pdf')
