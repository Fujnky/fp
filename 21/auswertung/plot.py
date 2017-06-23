import matplotlib.pyplot as plt
import  numpy as np

a,b,c,t1,I1,z = np.genfromtxt('daten/I1.csv', unpack=True, delimiter=',')
a,b,c,t2,I2,z = np.genfromtxt('daten/I2.csv', unpack=True, delimiter=',')
a,b,c,t3,U3,z = np.genfromtxt('daten/U1.csv', unpack=True, delimiter=',')
a,b,c,t4,U4,z = np.genfromtxt('daten/U2.csv', unpack=True, delimiter=',')
a,b,c,t5,U5,z = np.genfromtxt('daten/U3.csv', unpack=True, delimiter=',')

#plt.plot(t1, I1, '.')
t = (t2+1.1)/2

plt.xlim(0, 1)
lims = [[650, 800], [1180, 1290], [1400, 1600]]
plt.plot(t, I2/100, 'x', markersize=2)
plt.plot(t[lims[2][0]:lims[2][1]], U5[lims[2][0]:lims[2][1]], 'x', markersize=2)

plt.show()
