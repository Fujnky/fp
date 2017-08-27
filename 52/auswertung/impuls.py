import matplotlib.pyplot as plt
import numpy as np


x1=[0, 4, 0]
y1=[0, 2, 4]

x2=[0,8,0]
y2=[0,4,8]

x3=[0,4,8]
y3=[4,6,8]

xlabels=['$z$','$L_1$', '$L_2$']
x=[1,4,8]

ylabels=['$t_1$','$T$','$2T$', '$3T$', '$4T$']
y=[0.5,2,4,6,8]

zx=[1,1,1]
zy=[0,4,9]
tx=[0,1]
ty=[0.5,0.5]

plt.xlim(0,8)
plt.ylim(0,8.5)
plt.xticks(x, xlabels)
plt.yticks(y, ylabels)
plt.plot(zx,zy,'C1--')
plt.plot(tx,ty,'C1--')
plt.plot(x1,y1, 'C0-')
plt.plot(x2,y2, 'C0-')
plt.plot(x3,y3, 'C0--')

plt.savefig('impuls.pdf')
