import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit

c = const.c / np.sqrt(2.25)

def expo(t, a, b, c, d):
    return a * np.exp(b*t - c) + d

def ausw(name, zeiten, offset_kurzg, fit):
    bla,bla,bla,t1,U1,bla = np.genfromtxt('daten/'+name+'/offen.csv', unpack=True, delimiter=',')
    bla,bla,bla,t2,U2,bla = np.genfromtxt('daten/'+name+'/kurzgeschlossen.csv', unpack=True, delimiter=',')

    plt.xlabel(r'$t/\mathrm{µs}$')
    plt.ylabel(r'$U/\mathrm{V}$')
    plt.ylim(U1.min(), U1.max()+5)
    plt.xlim(1e6*t1.min(), 1e6*t1.max())
    plt.plot(1e6*np.ones(2)*zeiten[0], (U1.min(), U1.max()+5), 'k-', label='Laufzeit')
    plt.plot(1e6*np.ones(2)*zeiten[1], (U1.min(), U1.max()+5), 'k-')
    plt.plot(t1*1e6, U1, 'x', alpha=0.4, markersize=1.5, label='Messdaten')

    if fit:
        t1_ = t1[t1>zeiten[1]+2e-8]
        U1_ = U1[t1>zeiten[1]+2e-8]

        params1, pcov1 = curve_fit(expo, t1_, U1_, maxfev=100000000, p0=[2.59086446e+01,-1.53371705e+07,-1.36201933e+01,6.06292849e+00])
        print(params1)
        print('C = {}nF'.format(1e9*-1/(50*params1[1])))
        t1_ = np.linspace(t1_.min()-1e-6, t1_.max()+1e-6, 1000)
        plt.plot(1e6*t1_, expo(t1_, *params1), label='Exponentieller Fit')

    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/'+name+'_offen.pdf')
    plt.close()

    plt.xlabel(r'$t/\mathrm{µs}$')
    plt.ylabel(r'$U/\mathrm{V}$')
    plt.ylim(U2.min(), U2.max()+5)
    plt.xlim(1e6*t2.min(), 1e6*t2.max())
    plt.plot(1e6*np.ones(2)*zeiten[0]+1e6*offset_kurzg, (U2.min(), U2.max()+5), 'k-', label='Laufzeit')
    plt.plot(1e6*np.ones(2)*zeiten[1]+1e6*offset_kurzg, (U2.min(), U2.max()+5), 'k-')
    plt.plot(1e6*t2, U2, 'x', alpha=0.4, markersize=1.5, label='Messdaten')

    if fit:
        t2_ = t2[t2>zeiten[1]+offset_kurzg+2e-8]
        U2_ = U2[t2>zeiten[1]+offset_kurzg+2e-8]

        params2, pcov2 = curve_fit(expo, t2_, U2_, maxfev=100000000)#, p0=[50, 1e6, 0, 1])
        print(params2)
        print('L = {}µH'.format(1e6*-50/params2[1]))
        t2_ = np.linspace(t2_.min()-1e-6, t2_.max()+1e-6, 1000)
        plt.plot(1e6*t2_, expo(t2_, *params2), label='Exponentieller Fit')

    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/'+name+'_kurzgeschlossen.pdf')
    plt.close()

    print(name)
    t = (zeiten[1]-zeiten[0])
    print('{}ns'.format(t*1e9))
    print('{}m'.format(c * t / 2))


ausw('langes_kabel', (-9e-7, -4e-8), 8.7e-7, True)
ausw('mittleres_50ohm', (-1.7e-7, -0.7e-7), 0, False)
ausw('mittleres_75ohm', (-1.4e-7, -0.4e-7), 0, False)
