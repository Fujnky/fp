# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import scipy.stats
import uncertainties as unc
import uncertainties.unumpy as unp
import tools

data = np.genfromtxt('daten/daten.txt', dtype=object, unpack=True)
f, I11, I12, I21, I22 = data.astype(float)

f *= 1e6


def helmholtz(I, N, r):
    return 8/np.sqrt(125) * const.mu_0 * N * I / r


def auswerten(I1, I2, i, Z):

    B = helmholtz(I1, 11, 16.39e-2) + helmholtz(I2, 154, 15.79e-2)
    plt.plot(f/1e6, B*1e6, 'C{}x'.format(i),
             label=r'Messdaten von $^{'+Z+r'}\mathrm{Rb}$')

    x = f
    y = B
    slope, intercept, r, prob2, see = scipy.stats.linregress(x, y)
    mx = x.mean()
    sx2 = ((x-mx)**2).sum()
    sd_intercept = see * np.sqrt(1./len(x) + mx*mx/sx2)
    sd_slope = see * np.sqrt(1./sx2)
    f_syn = np.linspace(0, 1.1)
    plt.plot(f_syn, 1e6*(slope*f_syn*1e6+intercept),
             label='Lineare Regression')
    slope = unc.ufloat(slope, sd_slope)
    intercept = unc.ufloat(intercept, sd_intercept)
    # print('slope: {}µT/MHz, intercept: {} µT'.format(
    #    slope*1e6, intercept*1e6))

    g = 1/(slope / const.h * const.value('Bohr magneton'))
    print('g-Faktor Rb-{}: {}'.format(Z, g))
    print('Kernspin Rb-{}: {}'.format(Z, 1/(2*g)- 0.5))

    return g, slope, intercept, B


g1, slope1, emf1, B1 = auswerten(I11, I12, 0, '87')
g2, slope2, emf2, B2 = auswerten(I21, I22, 1, '85')

print((I11, I12, B1*1e6, I21, I22, B2*1e6))
tools.table((*data[:3], B1*1e6, *data[3:], B2*1e6),
            ('f/MHz',
             'I_1^\mathrm{sweep}/A',
             'I_1^\mathrm{hor}/A',
             r'B_1/\micro\tesla',
             'I_2^\mathrm{sweep}/A',
             'I_2^\mathrm{hor}/A',
             r'B_2/\micro\tesla'), 'build/feld.tex',
             'Bestimmte Stromstärken der jeweiligen Resonanzstellen und daraus berechnete magnetische Flussdichten.',
             'tab:feld')

emf = unc.ufloat(np.mean((emf1.n, emf2.n)), np.std((emf1.n, emf2.n)))

print('Gemitteltes Horizontalkomponente des Erdmagnetfelds: {}µT'.format(
                                                                1e6*emf))

print('Kompensiertes Vertikalfeld: {}µT'.format(
      helmholtz(0.23, 20, 11.735e-2)*1e6))
plt.xlabel(r'$f/\mathrm{MHz}$')
plt.ylabel(r'$B/\mathrm{µT}$')
plt.xlim(0, 1.1)
t = list(plt.yticks()[0])
plt.yticks(t + [emf.n*1e6],
           ['{0:8.0f}'.format(ti) for ti in t]+[r'$B_\mathrm{hor}^\oplus$'])

plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/plot1.pdf')
plt.close()


plt.xlabel(r'$f/\mathrm{MHz}$')
plt.ylabel(r'$B/\mathrm{µT}$')
plt.xlim(0, 1.1)

plt.plot(f/1e6, (B1-f*slope1.n-emf1.n)*1e6, 'x')
plt.plot(f/1e6, (B2-f*slope2.n-emf2.n)*1e6, 'x')

plt.savefig('build/plot3.pdf')
