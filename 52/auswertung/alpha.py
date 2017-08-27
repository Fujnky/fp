import numpy as np
import matplotlib.pyplot as plt
import peakdetect as peak


bla,bla,bla,f1,u1,bla = np.genfromtxt('daten/alpha_lang.csv', unpack=True, delimiter=',')
bla,bla,bla,f2,u2,bla = np.genfromtxt('daten/alpha_kurz.csv', unpack=True, delimiter=',')


p1 = peak.peakdetect(u1, f1, 1)
p2 = peak.peakdetect(u2, f2, 3)

plt.plot(f1, u1, '-')
plt.plot(f2, u2, '-')


p1 = np.array(p1[0]).T
p2 = np.array(p2[0]).T

p1 = p1.T[np.ma.mask_or(p1[1] > -15, np.logical_and(p1[0] > 1.1050e7, p1[0] < 1.1075e7))].T
p2 = p2.T[p2[1] > -15].T


plt.plot(p1[0], p1[1], 'C0x')
plt.plot(p2[0], p2[1], 'C1x')

print(p1[1]-p2[1])
plt.show()
