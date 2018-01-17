# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:22:12 2015

@author: Charles
"""
from __future__ import division

from past.utils import old_div
import numpy as np
import matplotlib.pyplot as plt



k = 0.1 #CGS
V = 1 #cm3
L = np.logspace(-1,1,50) #cm

rapport = 1 - (k * V / L**3) + (k**2 * V**2 / L**6)

plt.loglog(L,rapport,'k-',lw=1.5)
plt.ylabel('$\eta$')
plt.xlabel('Distance L (cm)')
plt.title('QUESTION 4')
plt.savefig('Question4')

plt.figure()

L = np.linspace(0,50,50) #cm
rapport = 1 - (k * V / L**3) + (k**2 * V**2 / L**6)

N = old_div(((old_div(1, rapport)) - 1),k)

plt.semilogy(L,N,'k-',lw=1.5)
plt.ylabel('N')
plt.xlabel('Distance L (cm)')
plt.title('QUESTION 5')
plt.savefig('Question5')
