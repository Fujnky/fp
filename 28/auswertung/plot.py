import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats
import tools
import uncertainties as unc
import uncertainties.unumpy as unp

# An den Leser: Das hier ist nicht besonders sinnvoll, wenn man den Versuch
# richtig durchgeführt hat.

liste = ['a', 'c', 'd', 'e']
p0liste = [[3000, 50, 300, 220], [-3000, 50, 400, 220], [3000, 50, 600, 220],
           [3000, 50, 750, 220]]

f = np.array((10.62e6, 20.56e6, 25e6, 29.423e6, 15.9037e6))


def cauchy(x, A, s, t, b):
    return A * (s/(s**2 + (x-t)**2))+b

def auswerten(param):
    name, p0 = param
    I1, U1 = np.genfromtxt('daten/'+name+'1.txt', unpack=True)
    I2, U2 = np.genfromtxt('daten/'+name+'2.txt', unpack=True)

    popt1, pcov1 = curve_fit(cauchy, I1, U1, maxfev=10000000, p0=p0)
    popt2, pcov2 = curve_fit(cauchy, I2, U2, maxfev=10000000, p0=p0)

    x = np.linspace(0, 950, 1000)
    plt.xlim(0, 950)
    plt.xlabel(r'$I/\mathrm{mA}$')
    plt.ylabel(r'$U_B / \mathrm{mV}$')
    plt.plot(x, cauchy(x, *popt1), 'C0', label="Fit (mod. Cauchy/Lorentz)")
    plt.plot(x, cauchy(x, *popt2), 'C1', label="Fit (mod. Cauchy/Lorentz)")
    plt.plot(I1, U1, 'x', label='Daten 1')
    plt.plot(I2, U2, 'x', label='Daten 2')
    plt.legend(loc='best')
    plt.tight_layout(pad=0)
    plt.savefig('build/'+name+'.pdf')
    plt.close()
    param1 = unc.correlated_values(popt1, pcov1)
    param2 = unc.correlated_values(popt2, pcov2)

    return param1[2], param2[2]


I = np.array(list(map(auswerten, zip(liste, p0liste)))).T/1e3


tools.table((f[:-1]/1e6, I[0]*1e3, I[1]*1e3), ('f/MHz', 'I_1/mA', 'I_2/mA'), 'build/ergfit.tex', 'Ermittelte Extremstellen, entsprechen der Resonanzfeldstärke.', 'tab:ergfit')

data_kal = np.genfromtxt('daten/kal.txt', dtype=object).T
tools.table(data_kal, ('l/mm', 'I/mA'), 'build/kal.tex', 'Daten der XY-Schreiber-Kalibrierung.', 'tab:kal')
kal_l, kal_i = data_kal.astype(float)


#m, n, r, p, std = scipy.stats.linregress(kal_l, kal_i)
z, cov = np.polyfit(kal_l, kal_i, 1, cov=True)

m = unc.ufloat(z[0], np.sqrt(cov[0][0]))
n = unc.ufloat(z[1], np.sqrt(cov[1][1]))

x = np.linspace(0, 210)
plt.plot(kal_l, kal_i, 'x', label='Kalibrierung XY-Schreiber')
plt.plot(x, m.n * x + n.n, label='Lin. Regression')
plt.xlim(0, 210)
plt.xlabel(r'$l/\mathrm{mm}$')
plt.ylabel(r'$I/\mathrm{mA}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/kal.pdf')
plt.close()

l = np.array((124.5, 145))
I_xy = (m*l+n)/1e3

I = np.append(I.T, [I_xy], axis=0).T
Ig = np.mean(I, axis=0)
dI = I[1]-I[0]

Bg = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * Ig
#g = - const.h * f / (Bg * (0.5 * const.e / const.m_e * const.hbar))
dB = const.mu_0 * 8 / np.sqrt(125) * 156/0.1 * dI

#print(dB)

z, cov = np.polyfit(f, unp.nominal_values(Bg), 1, cov=True, w=1/unp.std_devs(Bg))
m = unc.ufloat(z[0], np.sqrt(cov[0][0]))
n = unc.ufloat(z[1], np.sqrt(cov[1][1]))

f_ = np.linspace(0, 30e6)
B_fit = m.n*f_+n.n

plt.xlim(0, 30)
plt.ylim(0, 1100)
plt.plot(f_/1e6, B_fit*1e6, label='Lineare Regression')
plt.errorbar(f/1e6, unp.nominal_values(Bg)*1e6, yerr=unp.std_devs(Bg)*1e6, fmt='x', label='Messdaten')
plt.legend(loc='best')
plt.xlabel(r'$f/\mathrm{MHz}$')
plt.ylabel(r'$B/\mathrm{µT}$')
plt.tight_layout(pad=0)
plt.savefig('build/plotg.pdf')

print(const.h / (m * const.value('Bohr magneton')))
print(n*1e6)



tools.table((f/1e6, Bg*1e6, dB*1e6), ('f/MHz', r'B/\micro\tesla', r'B_\bigoplus/\micro\tesla'), 'build/ergg.tex', r'Berechnete Messergebnisse.', 'tab:ergg')

#print(g.mean(), g.std(ddof=1))
#print('{}+-{} µT'.format(dB.mean()*1e6, dB.std(ddof=1)*1e6))
