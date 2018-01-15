# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:52:12 2017

@author: Charles
"""
from __future__ import division

from future import standard_library
standard_library.install_aliases()
from builtins import object
from past.utils import old_div
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter.filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import numpy as np
from platform import system

plt.rcParams.update({'xtick.direction': 'out'})
plt.rcParams.update({'ytick.direction': 'out'})

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


def make_data():
    N = 100
    x = np.linspace(0, 2000, N)
    y = np.linspace(0, 1000, N)
    X, Y = np.meshgrid(x, y)
    
    # Mean vector and covariance matrix
    mu = np.array([1250., 600.])
    Sigma = np.array([[ 10000. , -10000], [-10000,  30000]])
    
    # Pack X and Y into a single 3-dimensional array
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y
    
    np.random.seed(5)
    elev = np.random.uniform(0,222,(len(X), len(Y)))
    elev = filters.gaussian_filter(elev, 7e0)
    tim = np.linspace(0,8,len(X)*len(Y)).reshape((len(X),len(Y)))
    
    # The distribution on the variables X, Y packed into pos.
    #Z = 1e4*multivariate_normal(pos, mu, Sigma)
    Z = multivariate_normal(mu, Sigma)
    Z = 1e5*Z.pdf(pos)
    #plt.contourf(X, Y, Z)
    #Z = 1e4*np.random.multivariate_normal(mu, Sigma, N*N)
    
    Z = add_altitude(Z, elev, elev[0,0])
    Z = add_plateau(Z, elev, elev[0,0], 2.66999)
    Z = add_derive(Z, tim)
    Z = add_latitude(Z, Y, 48.5333)
    return X, Y, Z, elev, tim

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
    
class MainApplication(object):
    def __init__(self, master):
        self.master = master
        # Séparer les colonnes
        # Construire l'interface
        self.make_frames()
        self.make_buttons()
        self.build_menu()
        
        self.fig_grav, self.ax_grav = plt.subplots(figsize=(6,3))
        self.cax_grav = make_axes_locatable(self.ax_grav).append_axes("right", size="5%", pad="2%")
        
#        self.fig_grav_i, self.ax_grav_i = plt.subplots(figsize=(6,3))
#        self.cax_grav_i = make_axes_locatable(self.ax_grav_i).append_axes("right", size="5%", pad="2%")
        
        self.fig_topo, self.ax_topo = plt.subplots(figsize=(6,3))
        self.cax_topo = make_axes_locatable(self.ax_topo).append_axes("right", size="5%", pad="2%")

        self.get_data()
        self.plot_topo()
        self.plot_grav()
#        self.plot_grav_i()
        self.draw_canvas()
        self.update_plots()
    
    def get_data(self):
        # Importer les donnees
        # Our 2-dimensional distribution will be over variables X and Y        
        self.elev = elev
        self.time = tim
        self.X, self.Y, self.g = X, Y ,Z
        
    def plot_topo(self):
        ct = self.ax_topo.contourf(self.X, self.Y, self.elev, cmap=cm.terrain, 
                                   levels=np.linspace(self.elev.min(), self.elev.max(), 50))
        self.ax_topo.contour(self.X, self.Y, self.elev, colors='k')
        self.fig_topo.colorbar(ct, cax=self.cax_topo, label='Élévation (m)', format='%d')
        self.ax_topo.set_xlim([self.X.min(), self.X.max()])
        self.ax_topo.set_ylim([self.Y.min(), self.Y.max()])
        self.ax_topo.set_xlabel("X (m)")
        self.ax_topo.set_ylabel("Y (m)")
        self.ax_topo.set_aspect('equal')
        self.ax_topo.grid('off')
        self.fig_topo.tight_layout()
        plt.close(self.fig_topo)
        
    def plot_grav(self):
        ct = self.ax_grav.contourf(self.X, self.Y, self.g, cmap=cm.coolwarm,
                                   levels=np.linspace(self.g.min(), self.g.max(), 50))
        self.ax_grav.contour(self.X, self.Y, self.g, colors='k')
        self.fig_grav.colorbar(ct, cax=self.cax_grav, label='Gravité (mGal)', format='%.1f')
        self.ax_grav.set_xlim([self.X.min(), self.X.max()])
        self.ax_grav.set_ylim([self.Y.min(), self.Y.max()])
        self.ax_grav.set_xlabel("X (m)")
        self.ax_grav.set_ylabel("Y (m)")
        self.ax_grav.set_aspect('equal')
        self.ax_grav.grid('off')
        self.fig_grav.tight_layout()
        plt.close(self.fig_grav)
    
#    def plot_grav_i(self):
#        ct = self.ax_grav_i.contourf(self.X, self.Y, self.g, cmap=cm.Greys)
#        self.ax_grav_i.contour(self.X, self.Y, self.g, colors='k')
#        self.fig_grav_i.colorbar(ct, cax=self.cax_grav_i, label='Gravité (mGal)', format='%.1f')
#        self.ax_grav_i.set_xlim([self.X.min(), self.X.max()])
#        self.ax_grav_i.set_ylim([self.Y.min(), self.Y.max()])
#        self.ax_grav_i.set_xlabel("X (m)")
#        self.ax_grav_i.set_ylabel("Y (m)")
#        self.ax_grav_i.set_aspect('equal')
#        self.ax_grav_i.grid('off')
#        self.fig_grav_i.tight_layout()
#        plt.close(self.fig_grav_i)
    
    def update_plots(self):
        self.fig_grav.canvas.draw() # Retrace le graphique
#        self.fig_grav_i.canvas.draw() # Retrace le graphique
        self.fig_topo.canvas.draw() # Retrace le graphique

    def update_grav_plot(self):
        self.ax_grav.clear()
        self.cax_grav.clear()
        self.plot_grav()
        self.fig_grav.canvas.draw() # Retrace le graphique
        
    def reset_plot(self):
        self.get_data()
        self.update_grav_plot()
        self.but_reset.config(state=tk.DISABLED)
        self.but_derive.config(state=tk.NORMAL)
        self.but_latitude.config(state=tk.NORMAL)
        self.but_altitude.config(state=tk.NORMAL)
        self.but_plateau.config(state=tk.NORMAL)   
        
    def app_derive(self):
        self.g = cor_derive(self.g, self.time)
        self.update_grav_plot()
        self.but_derive.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.NORMAL)
        
    def app_latitude(self):
        self.g = cor_latitude(self.g, self.Y, 48.5333)
        self.update_grav_plot()
        self.but_latitude.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.NORMAL)
        
    def app_altitude(self):
        self.g = cor_altitude(self.g, self.elev, self.elev[0,0])
        self.update_grav_plot()
        self.but_altitude.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.NORMAL)
        
    def app_plateau(self):
        self.g = cor_plateau(self.g, self.elev, self.elev[0,0], 2.67001)
        self.update_grav_plot()
        self.but_plateau.config(state=tk.DISABLED)   
        self.but_reset.config(state=tk.NORMAL)
        
    def make_frames(self):
        #==============================================================================
        # Build GUI by calling the main GUI functions
        self.frame_bout = tk.LabelFrame(self.master, text="Corrections", font=("TkDefaultFont", 12, "bold"))
        self.frame_bout.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,5), pady=5)
        self.frame_grav = tk.LabelFrame(self.master, text="Réponse gravimétrique corrigée", font=("TkDefaultFont", 12, "bold"))
        self.frame_grav.grid(row=1, column=1, columnspan=1, sticky=tk.W+tk.E+tk.N, padx=5, pady=5)
#        self.frame_grav_i = tk.LabelFrame(self.master, text="Réponse gravimétrique initiale", font=("TkDefaultFont", 12, "bold"))
#        self.frame_grav_i.grid(row=0, column=2, sticky=tk.W+tk.E+tk.N, padx=5, pady=5)
        self.frame_topo = tk.LabelFrame(self.master, text="Stations et topographie", font=("TkDefaultFont", 12, "bold"))
        self.frame_topo.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N, padx=5, pady=5)
        
    def make_buttons(self):
        self.but_altitude = tk.Button(self.frame_bout, text="Altitude", command=self.app_altitude)
        self.but_altitude.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_plateau = tk.Button(self.frame_bout, text="Plateau", command=self.app_plateau)
        self.but_plateau.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)     
        self.but_latitude = tk.Button(self.frame_bout, text="Latitude", command=self.app_latitude)
        self.but_latitude.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_derive = tk.Button(self.frame_bout, text="Dérive", command=self.app_derive)
        self.but_derive.grid(row=4, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_reset = tk.Button(self.frame_bout, text="Reset", command=self.reset_plot)
        self.but_reset.grid(row=5, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_reset.config(state=tk.DISABLED) # Bouton reset initialement désactivé

    def build_menu(self):
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.get_file_list)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

    def draw_canvas(self):
        # Trace la figure sur le canvas
        canvas_grav = FigureCanvasTkAgg(self.fig_grav, master=self.frame_grav)
        canvas_grav.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=(10,10), pady=(10,10))
        canvas_grav.show()
#         Ajoute une barre d'outils
        grav_toolbar_frame = tk.Frame(self.frame_grav)
        grav_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
        NavigationToolbar2TkAgg(canvas_grav, grav_toolbar_frame)

#        canvas_grav_i = FigureCanvasTkAgg(self.fig_grav_i, master=self.frame_grav_i)
#        canvas_grav_i.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=(10,10), pady=(10,10))
#        canvas_grav_i.show()
##         Ajoute une barre d'outils
#        grav_i_toolbar_frame = tk.Frame(self.frame_grav_i)
#        grav_i_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
#        NavigationToolbar2TkAgg(canvas_grav_i, grav_i_toolbar_frame)

#         Trace la figure sur le canvas
        canvas_topo = FigureCanvasTkAgg(self.fig_topo, master=self.frame_topo)
        canvas_topo.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=(10,10), pady=(10,10))
        canvas_topo.show()
#         Ajoute une barre d'outils
        topo_toolbar_frame = tk.Frame(self.frame_topo)
        topo_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
        NavigationToolbar2TkAgg(canvas_topo, topo_toolbar_frame)

    def get_file_list(self):
        # Va chercher une liste de fichier à ouvrir
        files = tkinter.filedialog.askopenfilenames(parent=self.master,title='Choose a file')
        self.open_files = sorted(list(files))
        self.get_data()
        self.plot_topo()
        self.plot_grav()
        self.draw_canvas()
        self.update_plots()
        
#==============================================================================
# Main function
#==============================================================================
X, Y, Z, elev, tim = make_data()
def main():
    root = tk.Tk()
    root.wm_title("Corrections gravimétriques")
    #==============================================================================
    # For MacOS, bring the window to front
    # Without these lines the application will start in background
    root.lift()
    if "Darwin" in system():
        root.call('wm', 'attributes', '.', '-topmost', True)
        root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
    MainApplication(root)
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    root.mainloop()
if __name__ == '__main__':
    main()
