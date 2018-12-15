#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:58:17 2018

@author: Charles
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import filters

data = np.loadtxt('cavite.dat', delimiter=',')

np.random.seed(17)
elev = np.random.uniform(0,100,len(data))
elev = filters.gaussian_filter(elev, 7e0)

# Altitude
def add_altitude(g, h, h_0):
    return g - 0.3086*(h-h_0)

# Plateau
def add_plateau(g, h, h_0, rho):
    return g + 0.04191*rho*(h-h_0)

def cor_altitude(g, h, h_0):
    return g + 0.3086*(h-h_0)

# Plateau
def cor_plateau(g, h, h_0, rho):
    return g - 0.04191*rho*(h-h_0)




rho = np.mean([2.93, 2.89, 2.91, 2.91, 2.89, 2.88, 2.90, 2.92, 2.90, 2.88])

#fig, ax = plt.subplots(1,2, figsize=(8,3))
#
##data[:,1] = add_altitude(data[:,1], elev, elev[0])
##data[:,1] = add_plateau(data[:,1], elev, elev[0], rho)
#
#plt.axes(ax[0])
#plt.plot(data[:,0], elev)
#plt.xlabel('Position (m)')
#plt.ylabel('Élévation (m)')
#
#plt.axes(ax[1])
#plt.plot(data[:,0], data[:,1])
#plt.xlabel('Position (m)')
#plt.ylabel('Gravité (mGal)')
#
#plt.tight_layout()
#plt.savefig('cavite_elev.pdf', dpi=600)

#data[:,1] = cor_altitude(data[:,1], elev, elev[0])

data = data[::2,:2]

data[:,1] += np.random.normal(0, 0.0005, len(data))


def grav_sphere(x, rho, r, p_x, p_z):
    G=6.67408e-11
    g = 1e5*((4/3)*np.pi*G*rho*p_z*r**3) / ( ((p_x - x)**2 + p_z**2)**(3./2) )
    return g

fig, ax = plt.subplots(figsize=(4,3))
plt.plot(data[:,0], data[:,1],'k.', label='Données')
plt.xlabel('Position (m)')
plt.ylabel('Gravité (mGal)')
plt.plot(data[:,0], -grav_sphere(data[:,0], 1000*rho-1000, 6.7, 97, 29), label='Modèle')
plt.legend(framealpha=1)
plt.savefig('cavite_elev.pdf', dpi=600, bbox_inches='tight')

#data = np.hstack((data,elev[:,np.newaxis]))

np.savetxt('cavite2018.dat', data, delimiter=',', comments='', header='position_m, gravite_mGal, altitude')
