import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit
from smithplot import SmithAxes
import tools

pa1 = np.empty((3,4))
pa2 = np.empty((3,4))
La = np.empty((3))
Ca = np.empty((3))

c = const.c / np.sqrt(2.25)

def expo(t, a, b, c, d):
    return a * np.exp(b*t - c) + d

def ausw(name, zeiten, offset_kurzg, fit, num):
    global pa1, pa2, La, Ca
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
        t1_ = t1[np.logical_and(t1>zeiten[2], t1<zeiten[4])]
        U1_ = U1[np.logical_and(t1>zeiten[2], t1<zeiten[4])]
        plt.plot(1e6*np.ones(2)*zeiten[2], (U1.min(), U1.max()+5), 'k--', alpha=0.5)
        plt.plot(1e6*np.ones(2)*zeiten[4], (U1.min(), U1.max()+5), 'k--', alpha=0.5)

        params1, pcov1 = curve_fit(expo, t1_, U1_, maxfev=100000000, p0=[2.59086446e+01,-1.53371705e+07,-1.36201933e+01,6.06292849e+00])
        pa1[num] = params1
        C = -1/(50*params1[1])
        Ca[num] = C
        #print('C = {}nF'.format(1e9*C))
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
        t2_ = t2[np.logical_and(t2>zeiten[3], t2<zeiten[5])]
        U2_ = U2[np.logical_and(t2>zeiten[3], t2<zeiten[5])]
        plt.plot(1e6*np.ones(2)*zeiten[3], (U1.min(), U1.max()+5), 'k--', alpha=0.5)
        plt.plot(1e6*np.ones(2)*zeiten[5], (U1.min(), U1.max()+5), 'k--', alpha=0.5)

        params2, pcov2 = curve_fit(expo, t2_, U2_, maxfev=100000000, p0=[2.59086446e+01,-1.53371705e+07,-1.36201933e+01,6.06292849e+00])
        pa2[num] = params2
        L = -50/params2[1]
        #print('L = {}µH'.format(1e6*L))
        La[num] = L
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

    '''if fit:
        #Schmissscharts
        plt.figure(figsize=(5,5))
        ax = plt.subplot(1, 1, 1, projection='smith')
        #plt.plot([10, 100], markevery=1)
        omega = 2* np.pi * np.linspace(2*1e3, 100*1e3, 20)
        X = omega * L - 1 / (omega * C)
        plt.plot((0+X*1j)/50, datatype=SmithAxes.Z_PARAMETER, label='Muh')
        plt.plot((1e100+X*1j)/50, datatype=SmithAxes.Z_PARAMETER, label='Muh')

        plt.legend(loc='best')
        plt.tight_layout(pad=0)
        plt.savefig('build/'+name+'_smith.pdf')
        plt.close()'''

ausw('langes_kabel', (-9e-7, -4e-8, -2e-8, 8.5e-7, 1, 1), 8.7e-7, True, 0)
ausw('mittleres_50ohm', (-1.7e-7, -0.7e-7, -0.0e-7, 0.2e-7, 0.6e-7, 0.5e-7), 0, True, 1)
ausw('mittleres_75ohm', (-1.4e-7, -0.4e-7, 0.3e-7, 0.1e-7, 0.6e-7, 0.6e-7), 0, True, 2)

K ={0:'Langes Kabel', 1:'Mittleres 50 Ohm', 2:'Mittleres 75 Ohm'}
tools.table([*pa1.T, *pa2.T], ('a_1/V', 'b_1/\per\second', 'c_1', 'd_1/V', 'a_2/V', 'b_2/\per\second', 'c_2', 'd_2/V'), 'build/laufzeit.tex', 'Fitparameter.', 'tab:laufzeit', interrows=K)
tools.table((La*1e6, Ca*1e9), ('L/µH', 'C/nF'), 'build/laufzeit2.tex', 'Ergebnisse der Leitungsparameter.', 'tab:laufzeit2', interrows = K)
