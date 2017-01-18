# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:03:36 2017

@author: Charles
"""

import numpy as np
import matplotlib.pyplot as plt

axeX = np.arange(0,300)*100

G = 6.674e-8

rho_1 = 3.78
R_1 = 12.8*100
PosX_1 = 75*100
PosZ_1 = 19*100

rho_2 = -2.67
R_2 = 16.3*100
PosX_2 = 200*100
PosZ_2 = 23*100

rho_3 = 2.21
R_3 = 15.0
PosX_3 = 150
PosZ_3 = 20

rho_4 = -2.0
R_4 = 0.05
PosX_4 = 200
PosZ_4 = 5

def grav_cylindre(x, G, rho, r, p_x, p_z):
    return (2 * np.pi * G * rho * r**2) / (p_z * (1 + ((p_x - x)/p_z)**2))

def grav_sphere(x, G, rho, r, p_x, p_z):
    return (4./3)*np.pi*G*rho*p_z*r**3 / ( ((p_x - x)**2 + p_z**2)**(3./2) )
    
g_1 = grav_sphere(axeX, G, rho_1, R_1, PosX_1, PosZ_1)

g_2 = grav_sphere(axeX, G, rho_2, R_2, PosX_2, PosZ_2)

g_3 = grav_sphere(axeX, G, rho_3, R_3, PosX_3, PosZ_3)

g_4 = grav_cylindre(axeX, G, rho_4, R_4, PosX_4, PosZ_4)

g_data = g_1 + g_2 

g_data += np.random.normal(0,0.01*max(g),size=len(g))

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

g_model = []
#for i in range(1000):
    
while True:
    
    rho_mod_1 = np.random.uniform(0,5)
    R_mod_1 = np.random.uniform(5,15)
    
    rho_mod_2 = np.random.uniform(-5,5)
    R_mod_2 = np.random.uniform(5,15)
    
    print rho_mod_1
#    print rho_mod_2
    
    g_model.append(grav_sphere(axeX, G, rho_mod_1, R_1, PosX_1, PosZ_1) + grav_sphere(axeX, G, rho_2, R_2, PosX_2, PosZ_2))

    RMS = np.sqrt(((g_model - g_data) ** 2).mean())
    print RMS
    if RMS < 0.0003:
        break
    
    #    print np.sum(g_model-g_data)

#plt.plot(g_model[-1])
    
plt.plot(axeX/100, 1000*g_data, 'bo')
plt.plot(axeX/100, 1000*g_model[-1], 'r-')
plt.xlabel("Position")
plt.ylabel("mGal")