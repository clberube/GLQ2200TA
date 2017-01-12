# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:52:12 2017

@author: Charles
"""

import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkFileDialog
import matplotlib.pyplot as plt
import numpy as np
from platform import system

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
    
class MainApplication:
    def __init__(self, master):
        self.master = master
        # Séparer les colonnes
        # Construire l'interface
        self.make_frames()
        self.make_buttons()
        self.build_menu()
 
    def get_data(self):
        # Importer les donnees
        self.data = np.loadtxt(self.open_files[0], delimiter=",", skiprows=1)
        self.position = self.data[:,0]
        self.heure = self.data[:,1]
        self.g = self.data[:,2]
        self.altitude = self.data[:,3]
        
    def plot_topo(self):
        self.fig_topo = plt.figure()
        plt.plot(self.position[:-1], self.altitude[:-1], 'ko-')
        plt.xlim([0, 800])
        plt.xlabel("Position (m)")
        plt.ylabel("Altitude (m)")
        plt.close()
        
    def plot_grav(self):
        self.fig_grav, self.ax_grav = plt.subplots()
        self.ax_grav.scatter(self.position, self.g, alpha=0.5, s=25, facecolors='none', edgecolors='k')
        self.ax_grav.set_ylim([-1, 6])
        self.ax_grav.set_xlim([0, 800])
        self.reponse, = self.ax_grav.plot(self.position, self.g, 'bo')
        plt.xlabel("Position (m)")
        plt.ylabel(u"Gravité (mGal)")
        plt.close()
    
    def update_plot(self):
        self.reponse.set_ydata(self.g) # Remplace le data dans le graphique
        self.fig_grav.canvas.draw() # Retrace le graphique
        
    def reset_plot(self):
        self.g = self.data[:,2]
        self.update_plot()
        self.but_reset.config(state=tk.DISABLED)
        self.but_derive.config(state=tk.ACTIVE)
        self.but_latitude.config(state=tk.ACTIVE)
        self.but_altitude.config(state=tk.ACTIVE)
        self.but_plateau.config(state=tk.ACTIVE)   
        
    def app_derive(self):
        self.g = corr_derive(self.g, self.heure)
        self.update_plot()
        self.but_derive.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.ACTIVE)
        
    def app_latitude(self):
        self.g = corr_latitude(self.g, self.position, 48.5333)
        self.update_plot()
        self.but_latitude.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.ACTIVE)
        
    def app_altitude(self):
        self.g = corr_altitude(self.g, self.altitude)
        self.update_plot()
        self.but_altitude.config(state=tk.DISABLED)
        self.but_reset.config(state=tk.ACTIVE)
        
    def app_plateau(self):
        self.g = corr_plateau(self.g, self.altitude, 2.2)
        self.update_plot()
        self.but_plateau.config(state=tk.DISABLED)   
        self.but_reset.config(state=tk.ACTIVE)
        
    def make_frames(self):
        #==============================================================================
        # Build GUI by calling the main GUI functions
        self.frame_bout = tk.LabelFrame(self.master, text="Corrections", font=("TkDefaultFont", 12, "bold"))
        self.frame_bout.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,0), pady=10)
        self.frame_grav = tk.LabelFrame(self.master, text="Réponse gravimétrique", font=("TkDefaultFont", 12, "bold"))
        self.frame_grav.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.frame_topo = tk.LabelFrame(self.master, text="Stations et topographie", font=("TkDefaultFont", 12, "bold"))
        self.frame_topo.grid(row=0, column=2, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        
    def make_buttons(self):
        self.but_derive = tk.Button(self.frame_bout, text="Dérive", command=self.app_derive)
        self.but_derive.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_latitude = tk.Button(self.frame_bout, text="Latitude", command=self.app_latitude)
        self.but_latitude.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_plateau = tk.Button(self.frame_bout, text="Plateau", command=self.app_plateau)
        self.but_plateau.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_altitude = tk.Button(self.frame_bout, text="Altitude", command=self.app_altitude)
        self.but_altitude.grid(row=4, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
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
        canvas_grav.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        canvas_grav.show()
        # Ajoute une barre d'outils
        grav_toolbar_frame = tk.Frame(self.frame_grav)
        grav_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
        NavigationToolbar2TkAgg(canvas_grav, grav_toolbar_frame)
        # Trace la figure sur le canvas
        canvas_topo = FigureCanvasTkAgg(self.fig_topo, master=self.frame_topo)
        canvas_topo.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        canvas_topo.show()
        # Ajoute une barre d'outils
        topo_toolbar_frame = tk.Frame(self.frame_topo)
        topo_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
        NavigationToolbar2TkAgg(canvas_topo, topo_toolbar_frame)

    def get_file_list(self):
        # Va chercher une liste de fichier à ouvrir
        files = tkFileDialog.askopenfilenames(parent=self.master,title='Choose a file')
        self.open_files = sorted(list(files))
        self.get_data()
        self.plot_topo()
        self.plot_grav()
        self.draw_canvas()
        
#==============================================================================
# Main function
#==============================================================================
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
