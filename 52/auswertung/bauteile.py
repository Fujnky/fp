import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import tools

def expo(t, a, b, c, d):
    return a * np.exp(b*t - c) + d

pa = np.empty((3,4))

def plot(name, start_fit_at, num):
    bla,bla,bla,t,U,bla = np.genfromtxt('daten/bauteil'+name+'.csv', unpack=True, delimiter=',')
    plt.plot(t*1e6, U, 'x', alpha=0.2, markersize=4, label='Messdaten')
    plt.ylim(U.min()-1, U.max()+10)
    plt.xlim(t.min()*1e6, t.max()*1e6)

    if start_fit_at != None:
        t_ = t[t>start_fit_at]
        U_ = U[t>start_fit_at]

        plt.plot(np.ones(2)*start_fit_at*1e6, (U.min()-1, U.max()+10), 'k-', label="Beginn der Fit-Daten")
        params, pcov = curve_fit(expo, t_, U_, maxfev=100000000, p0=[5.75540096e-03, -5.50832242e+05, -1.02684351e+01, 4.81875157e+00])
        pa[num] = params
        plt.plot(t*1e6, expo(t, *params), 'C1', label='Exponentieller Fit')

    #plt.xlim(t.min(), t.max())
    plt.xlabel(r'$t/\mathrm{µs}$')
    plt.ylabel(r'$U/\mathrm{V}$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/bauteil'+name+'.pdf')
    plt.close()

    if start_fit_at != None:
        return params[1]

print("L = {}µH".format(-50/plot('3.5', 1.2e-6, 0)*1e6,))
print("L = {}µH".format(-50/plot('3.7', 0.87e-6, 1)*1e6))
print("C = {}nF".format(-1/(50*plot('3.10', 1.5e-6, 2))*1e9))

K ={0:'Induktivität', 1:'50 Ohm-Abschlusswiderstand', 2:'Kondensator'}
tools.table([*pa.T, *pa.T], ('a_1/V', 'b_1/\per\second', 'c_1', 'd_1/V', 'a_2/V', 'b_2/\per\second', 'c_2', 'd_2/V'), 'build/bauteile.tex', 'Fitparameter der Bauteile.', 'tab:bauteile', interrows=K)
