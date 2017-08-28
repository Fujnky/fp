import numpy as np
import matplotlib.pyplot as plt
import tools

data = np.genfromtxt('daten/rlc.txt', unpack=True, dtype=object)

f, C1, R1, L1, C2, R2, L2 = data.astype(float)
ω = 2 * np.pi * f

G1 = R1 * (C1/1e12) / (L1/1e6)
G2 = R2 * (C2/1e12) / (L2/1e6)

tools.table((data[0], data[2], data[5], data[3], data[6], data[1], data[4], G1*1e3, 1e3*G2), ('f/kHz', 'R_1/\ohm', 'R_2/\ohm', 'L_1/\micro\henry', 'L_2/\micro\henry', 'C_1/pF', 'C_2/pF', 'G_1/mS', 'G_2/mS'), 'build/rlcg.tex', 'Messdaten der ersten Messreihe.', 'tab:rlcg')

plt.figure(figsize=(6,8))

ax1 = plt.subplot(811)
plt.ylabel(r'$R_1/\mathrm{\Omega}$')
plt.plot(ω, R1, 'C0x')
plt.setp(ax1.get_xticklabels(), visible=False)

ax2 = plt.subplot(812, sharex=ax1)
plt.ylabel(r'$R_2/\mathrm{\Omega}$')
plt.plot(ω, R2, 'C0x')
plt.setp(ax2.get_xticklabels(), visible=False)

ax3 = plt.subplot(813, sharex=ax1)
plt.ylabel(r'$L_1/\mathrm{µH}$')
plt.setp(ax3.get_xticklabels(), visible=False)
plt.plot(ω, L1, 'C1x', )

ax4 = plt.subplot(814, sharex=ax1)
plt.ylabel(r'$L_2/\mathrm{µH}$')
plt.setp(ax4.get_xticklabels(), visible=False)
plt.plot(ω, L2, 'C1x')

ax5 = plt.subplot(815, sharex=ax1)
plt.ylabel(r'$C_1/\mathrm{pF}$')
plt.setp(ax5.get_xticklabels(), visible=False)
plt.plot(ω, C1, 'C2x')

ax6 = plt.subplot(816, sharex=ax1)
plt.ylabel(r'$C_2/\mathrm{pF}$')
plt.setp(ax6.get_xticklabels(), visible=False)
plt.plot(ω, C2, 'C2x')

ax7 = plt.subplot(817, sharex=ax1)
plt.ylabel(r'$G_1/\mathrm{mS}$')
plt.setp(ax7.get_xticklabels(), visible=False)
plt.plot(ω, G1*1e3, 'C3x')

ax8 = plt.subplot(818, sharex=ax1)
plt.ylabel(r'$G_2/\mathrm{mS}$')
plt.plot(ω, G2*1e3, 'C3x')

plt.xlabel(r'$\omega/\mathrm{kHz}$')
plt.tight_layout(pad=0)
plt.subplots_adjust(hspace=.1)
plt.savefig('build/rlcg.pdf')
