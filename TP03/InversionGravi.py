# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:03:36 2017

@author: Charles
"""

import numpy as np
import matplotlib.pyplot as plt

def grav_cylindre(x, rho, r, p_x, p_z, G=6.674e-8):
    return ((2 * np.pi * G * rho * r**2) / p_z ) / (1 + (((p_x - x)/p_z)**2))

def grav_sphere(x, rho, r, p_x, p_z, G=6.674e-8):
    return (4./3)*np.pi*G*rho*p_z*r**3 / ( ((p_x - x)**2 + p_z**2)**(3./2) )

# Axe des X et paramètres intiaux pour calculer la réponse des corps simples
axeX = np.arange(0,500)*100

rho_1 = 3.78
R_1 = 12.8*100
PosX_1 = 75*100
PosZ_1 = 19*100

rho_2 = -1.67
R_2 = 16.3*100
PosX_2 = 200*100
PosZ_2 = 23*100

rho_3 = -2.67
R_3 = 10.0*100
PosX_3 = 350*100
PosZ_3 = 21.5*100

# Générer le data synthétique à partir des paramètres initiaux
g_1 = grav_sphere(axeX, rho_1, R_1, PosX_1, PosZ_1)
g_2 = grav_sphere(axeX, rho_2, R_2, PosX_2, PosZ_2)
g_3 = grav_cylindre(axeX, rho_3, R_3, PosX_3, PosZ_3)
g_data = g_1 + g_2 + g_3
# Ajouter un bruit Gaussien de 2%
g_data += np.random.normal(0,0.02*max(abs(g_data)),size=len(g_data)) 

# Générer des listes vides pour entreposer les paramètres choisis
param1 = []
param2 = []
param3 = []
RMS_list = []

# Tester N hypothèses et calculer la fonction objectif 
for i in range(100000):
    # Générer des paramètres de façon aléatoire
    rho_mod_1 = np.random.uniform(-5,5)
    R_mod_2 = np.random.uniform(10,20)*100
    PosZ_mod_3 = np.random.uniform(0,30)*100
    # Calculer le modèle proposé
    g_model = grav_sphere(axeX, rho_mod_1, R_1, PosX_1, PosZ_1) + grav_sphere(axeX, rho_2, R_mod_2, PosX_2, PosZ_2) + grav_cylindre(axeX, rho_3, R_3, PosX_3, PosZ_mod_3)
    # La fonction objectif (Root Mean Square Error)
    RMS = np.sqrt(((g_model - g_data) ** 2).mean()) 
    # Entreposer les paramètres si c'est la première itération ou si la 
    # nouvelle hypothèse est plus probable que la précédente
    if (i == 0) or (RMS < RMS_list[-1]):
        RMS_list.append(RMS)
        param1.append(rho_mod_1)
        param2.append(R_mod_2)
        param3.append(PosZ_mod_3)
   
# Tracer le graphique du meilleur modèle
for i in range(len(param1)):
    best_g_model = grav_sphere(axeX, param1[i], R_1, PosX_1, PosZ_1) + grav_sphere(axeX, rho_2, param2[i], PosX_2, PosZ_2) + grav_cylindre(axeX, rho_3, R_3, PosX_3, param3[i])
    plt.figure()
    plt.plot(axeX/100, 1000*g_data, 'bo')
    plt.plot(axeX/100, 1000*best_g_model, 'r-')
    plt.xlabel("Position")
    plt.ylabel("mGal")
    
plt.figure()
plt.plot(RMS_list)