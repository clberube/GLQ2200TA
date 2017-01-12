# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:52:12 2017

@author: Charles
"""

import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import numpy as np
from platform import system

# Importer les donnees
data = np.loadtxt("Tableau_donnees_TP01_H2017.csv", delimiter=",", skiprows=1)

# Séparer les colonnes
position = data[:,0]
heure = data[:,1]
g = data[:,2]
altitude = data[:,3]

# Dérive
def corr_derive(g, t):
    tau = (g[-1] - g[0]) / (t[-1] - t[0])
    return g - tau*(t - t[0])

# Latitude
def corr_latitude(g, x, phi):
    return g + (8.1669e-4 * x * np.sin(np.deg2rad(2*phi)))

# Altitude
def corr_altitude(g, h):
    return g + 0.3086*(h-h[0])

# Plateau
def corr_plateau(g, h, rho):
    return g - 0.04191*rho*(h-h[0])

# Appliquer les corrections
#g_1 = corr_derive(g_3, heure)
#g_2 = corr_latitude(g, position, 48.5333)
#g_3 = corr_altitude(g_1, altitude)
#g_4 = corr_plateau(g_2, altitude, 2.2)

fig_topo = plt.figure()
plt.plot(altitude, 'ko-')
plt.xlabel("Position (m)")
plt.ylabel("Altitude (m)")

fig_grav, ax_grav = plt.subplots()
reponse, = ax_grav.plot(position, g, 'ro')
plt.xlabel("Position (m)")
plt.ylabel("Gravite (mGal)")

#plt.figure()
#plt.plot(g_4,'bo')
plt.close("all")

def reset_plot():
    global g
    g = data[:,2]
    reponse.set_ydata(g)
    plt.setp(reponse,'color','red')
    fig_grav.get_axes()[0].set_ylim([0.9*min(g), 1.1*max(g)])
    fig_grav.canvas.draw()

def app_derive():
    global g
    g = corr_derive(g, heure)
    reponse.set_ydata(g)
    plt.setp(reponse,'color','red')
    fig_grav.get_axes()[0].set_ylim([0.9*min(g), 1.1*max(g)])
    fig_grav.canvas.draw()
    
def app_latitude():
    global g
    g = corr_latitude(g, position, 48.5333)
    reponse.set_ydata(g)
    plt.setp(reponse,'color','red')
    fig_grav.get_axes()[0].set_ylim([0.9*min(g), 1.1*max(g)])
    fig_grav.canvas.draw()
    
def app_altitude():
    global g
    g = corr_altitude(g, altitude)
    reponse.set_ydata(g)
    plt.setp(reponse,'color','red')
    fig_grav.get_axes()[0].set_ylim([0.9*min(g), 1.1*max(g)])
    fig_grav.canvas.draw()

def app_plateau():
    global g
    g = corr_plateau(g, altitude, 2.2)
    reponse.set_ydata(g)
    plt.setp(reponse,'color','blue')
    fig_grav.get_axes()[0].set_ylim([0.9*min(g), 1.1*max(g)])
    fig_grav.canvas.draw()
   
    
#==============================================================================
# Window start
root = tk.Tk()
root.wm_title("Modelisation gravite 2D")
#==============================================================================
# Build GUI by calling the main GUI functions
frame_bout = tk.LabelFrame(root, text="Corrections", font=("TkDefaultFont", 14, "bold"))
frame_bout.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,0), pady=10)

frame_grav = tk.LabelFrame(root, text="Reponse gravimetrique", font=("TkDefaultFont", 14, "bold"))
frame_grav.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)

frame_topo = tk.LabelFrame(root, text="Stations et topographie", font=("TkDefaultFont", 14, "bold"))
frame_topo.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)

tk.Button(frame_bout, text="Derive", command=app_derive).grid(row=0, column=2, sticky=tk.W+tk.E+tk.N)
tk.Button(frame_bout, text="Latitude", command=app_latitude).grid(row=2, column=2, sticky=tk.W+tk.E+tk.N)
tk.Button(frame_bout, text="Altitude", command=app_altitude).grid(row=1, column=2, sticky=tk.W+tk.E+tk.N)
tk.Button(frame_bout, text="Plateau", command=app_plateau).grid(row=3, column=2, sticky=tk.W+tk.E+tk.N)
tk.Button(frame_bout, text="Reset", command=reset_plot).grid(row=4, column=2, sticky=tk.W+tk.E+tk.N)


canvas1 = FigureCanvasTkAgg(fig_grav, master=frame_grav)
canvas1.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
canvas1.show()
grav_toolbar_frame = tk.Frame(frame_grav)
grav_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
NavigationToolbar2TkAgg(canvas1, grav_toolbar_frame)

canvas2 = FigureCanvasTkAgg(fig_topo, master=frame_topo)
canvas2.get_tk_widget().grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
canvas2.show()
#topo_toolbar_frame = tk.Frame(frame_topo)
#topo_toolbar_frame.grid(row=1,column=0,columnspan=2, sticky=tk.W)
#NavigationToolbar2TkAgg(canvas2, topo_toolbar_frame)

#==============================================================================
# Window size options
root.resizable(width=tk.FALSE, height=tk.FALSE)
#==============================================================================
# For MacOS, bring the window to front
# Without these lines the application will start in background
if "Darwin" in system():
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', True)
    root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
#==============================================================================
# Window loop
tk.mainloop()
