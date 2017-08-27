import numpy as np
import matplotlib.pyplot as plt

f, C1, R1, L1, C2, R2, L2 = np.genfromtxt('daten/rlc.txt', unpack=True)
ω = 2 * np.pi * f

G1 = R1 / 50**2
G2 = R2 / 75**2


ax1 = plt.subplot(611)
plt.plot(ω, R1, 'x')
plt.setp(ax1.get_xticklabels(), visible=False)

ax2 = plt.subplot(612, sharex=ax1)
plt.plot(ω, R2, 'x')
plt.setp(ax2.get_xticklabels(), visible=False)

ax3 = plt.subplot(613, sharex=ax1)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.plot(ω, L1, 'x')

ax3 = plt.subplot(614, sharex=ax1)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.plot(ω, L2, 'x')

ax3 = plt.subplot(615, sharex=ax1)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.plot(ω, C1, 'x')

ax3 = plt.subplot(616, sharex=ax1)
plt.plot(ω, C2, 'x')
plt.show()
