# -*- coding: utf-8 -*-
"""
Local -v- Global min
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#inputs
X=np.linspace(0.1,1.1,50)
Y=[math.cos(3*math.pi*xi)/xi for xi in X]

#plot

plt.plot(X,Y,label="Formula: Cos(3*PI*X)/X")
plt.title("Global -v- Local minimum")

# description
plt.annotate('Local Minima',xy=(1,-0.5),xytext=(0.90,0.5),
             arrowprops=dict(arrowstyle='->',lw=1.5,color='r'),bbox=dict(pad=5,facecolor="none"))

plt.grid()
plt.savefig("minima.png")
plt.show()


