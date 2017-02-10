# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 21:38:55 2017

@author: Charles
"""

from __future__ import division
import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkFileDialog
import matplotlib.pyplot as plt
import numpy as np
from platform import system
import time

class MainApplication:
    def __init__(self, master):
        self.master = master
        # Séparer les colonnes
        # Construire l'interface
        self.duration = 1000
        self.time = np.arange(0, self.duration)
        self.make_frames()
        self.make_buttons()
        self.plot_reponse()
        self.plot_model()
        self.draw_canvas()

                
    def plot_reponse(self):
        self.fig_data, self.ax_data = plt.subplots(figsize=(6,3))
        self.reponse_dot, = self.ax_data.plot(0, 0, 'ro')
        self.reponse_line, = self.ax_data.plot(0, 0, 'k-')
        self.ax_data.set_ylim([-0.5, 0.1])
        self.ax_data.set_xlim([-self.duration/2, self.duration/2])
        plt.xlabel("Temps (minutes)")
        plt.ylabel("Gravite (mGal)")
        plt.close()
        
    def plot_model(self):
        self.fig_mod, self.ax_mod = plt.subplots(figsize=(6,3))
        self.ax_mod.plot([0,250], [20,20], 'k-')
        self.ax_mod.plot([250,250], [0,20], 'k-')
        self.ax_mod.plot([250,800], [15,15], 'k:')
#        self.model, = self.ax_mod.plot([250,800], [10,10], 'k-')
        arrow_props = dict(arrowstyle="->", fc='k', ec='k', 
                       )
        self.ax_mod.annotate(u'Gravimètre', xy=(225, 22), xytext=(25, 25), size=12,
                             arrowprops=arrow_props)
        self.ax_mod.plot([225,225], [22,20], 'k-')
        self.ax_mod.plot(225, 22, 'ro', markersize=10)
        self.ax_mod.fill_between([250,800], 0, 10)
        self.ax_mod.plot(0, 0, 'r-')
        self.ax_mod.set_ylim([0, 30])
        self.ax_mod.set_xlim([0, 800])
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.close()
        
    def plaque_mince(self, e, z, x):
        e = 100*e
        z = 100*z
        x = 100*x
        rho = -1.0
        G = 6.674e-8 # CGS
        g = 1000*2*G*rho*e*(np.pi/2 + np.arctan(x/z)) # mGal
        return g
        
    def animate(self):
        g_list = []
        for t in self.time:
            h = np.random.normal(0,0.1) + ((15-5)*np.sin(2*np.pi*t/540) + 15 + 5) / 2
#            self.model.set_ydata([h,h])
            epaisseur = 15 - h
            z = 15 - epaisseur/2
            g_list.append(self.plaque_mince(epaisseur, z, 25))
            for coll in (self.ax_mod.collections):
                self.ax_mod.collections.remove(coll)
            self.ax_mod.fill_between([250,800], 0, h)
            self.ax_mod.fill_between([250,800], h, 15, color="none", hatch="+", edgecolor="b", linewidth=0.0)
            self.fig_mod.canvas.draw()
            self.reponse_line.set_ydata(g_list[:t])
            self.reponse_line.set_xdata(self.time[:t])
            self.reponse_dot.set_ydata(self.plaque_mince(epaisseur, z, 25))
            self.reponse_dot.set_xdata(t)
            
            self.ax_data.set_xlim([t-self.duration/2, t+self.duration/2])
            self.fig_data.canvas.draw()
            
#            time.sleep(0.1)
            
    def make_frames(self):
        #==============================================================================
        # Build GUI by calling the main GUI functions
        self.frame_bout = tk.LabelFrame(self.master, text="Simulation", font=("TkDefaultFont", 12, "bold"))
        self.frame_bout.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,0), pady=10)
        self.frame_data = tk.LabelFrame(self.master, text="Réponse gravimétrique", font=("TkDefaultFont", 12, "bold"))
        self.frame_data.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.frame_rms = tk.LabelFrame(self.master, text="Modèle (Plaque mince semi-infinie)", font=("TkDefaultFont", 12, "bold"))
        self.frame_rms.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        
    def make_buttons(self):
        self.but_run = tk.Button(self.frame_bout, text="GO", command=lambda: self.animate())
        self.but_run.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_reset = tk.Button(self.frame_bout, text="Reset", command=lambda: self.empty_lists())
        self.but_reset.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)

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
        canvas_data = FigureCanvasTkAgg(self.fig_data, master=self.frame_data)
        canvas_data.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        canvas_data.show()
        # Ajoute une barre d'outils
#        grav_toolbar_frame = tk.Frame(self.frame_grav)
#        grav_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
#        NavigationToolbar2TkAgg(canvas_grav, grav_toolbar_frame)
        # Trace la figure sur le canvas
        canvas_mod = FigureCanvasTkAgg(self.fig_mod, master=self.frame_rms)
        canvas_mod.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        canvas_mod.show()
        # Ajoute une barre d'outils
#        topo_toolbar_frame = tk.Frame(self.frame_topo)
#        topo_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
#        NavigationToolbar2TkAgg(canvas_topo, topo_toolbar_frame)

#==============================================================================
# Main function
#==============================================================================
def main():
    root = tk.Tk()
    root.wm_title("Démo monitoring des marées et du niveau d'eau")
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