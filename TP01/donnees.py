#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 21:22:54 2018

@author: Charles
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.ndimage import filters
from scipy.stats import multivariate_normal

# Our 2-dimensional distribution will be over variables X and Y
N = 100
X = np.linspace(0, 1500, N)
Y = np.linspace(0, 1500, N)
X, Y = np.meshgrid(X, Y)

# Mean vector and covariance matrix
mu = np.array([1000., 1000.])
Sigma = np.array([[ 10000. , -10000], [-10000,  50000]])

# Pack X and Y into a single 3-dimensional array
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

np.random.seed(5)
elev = np.random.uniform(0,222,(len(X), len(Y)))
elev = filters.gaussian_filter(elev, 7e0)
tim = np.linspace(0,8,len(X)*len(Y)).reshape((len(X),len(Y)))

# Dérive
def cor_derive(g, t):
    tau = (1.2 - 1.0) / (t[-1,-1] - t[0,0])
    return g - tau*(t - t[0])

# Latitude
def cor_latitude(g, y, phi):
    return g + (8.1669e-4 * y * np.sin(np.deg2rad(2*phi)))

# Altitude
def cor_altitude(g, h, h_0):
    return g + 0.3086*(h-h_0)

# Plateau
def cor_plateau(g, h, h_0, rho):
    return g - 0.04191*rho*(h-h_0)

# Dérive
def add_derive(g, t):
    tau = (1.2 - 1.0) / (t[-1,-1] - t[0,0])
    return g + tau*(t - t[0])

# Latitude
def add_latitude(g, y, phi):
    return g - (8.1669e-4 * y * np.sin(np.deg2rad(2*phi)))

# Altitude
def add_altitude(g, h, h_0):
    return g - 0.3086*(h-h_0)

# Plateau
def add_plateau(g, h, h_0, rho):
    return g + 0.04191*rho*(h-h_0)

# The distribution on the variables X, Y packed into pos.
#Z = 1e4*multivariate_normal(pos, mu, Sigma)
Z = multivariate_normal(mu, Sigma)
Z = 1e5*Z.pdf(pos)
#plt.contourf(X, Y, Z)
#Z = 1e4*np.random.multivariate_normal(mu, Sigma, N*N)

# Create a surface plot and projected filled contour plot under it.
fig = plt.figure()
plt.contourf(X, Y, Z, cmap=cm.viridis)
plt.colorbar()

Z = add_altitude(Z, elev, elev[0,0])
Z = add_plateau(Z, elev, elev[0,0], 2.66)
Z = add_derive(Z, tim)
Z = add_latitude(Z, Y, 48.5333)

fig = plt.figure()
plt.contourf(X, Y, Z, cmap=cm.viridis)
plt.colorbar()

#Z = cor_altitude(Z, elev, elev[0,0])
#Z = cor_plateau(Z, elev, elev[0,0], 2.67)
#Z = cor_derive(Z, tim)
#Z = cor_latitude(Z, Y, 48.5333)
#
#fig = plt.figure()
#plt.contourf(X, Y, Z, cmap=cm.viridis)
#plt.colorbar()

#fig = plt.figure()
#plt.contourf(X, Y, elev, zdir='z', offset=-0.15, cmap=cm.viridis)
#plt.colorbar()