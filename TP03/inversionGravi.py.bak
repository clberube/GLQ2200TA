# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:03:36 2017

@author: Charles
"""

import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkFileDialog
import matplotlib.pyplot as plt
import numpy as np
from platform import system
import time

def grav_cylindre(x, rho, r, p_x, p_z, G=6.674e-8):
    return ((2 * np.pi * G * rho * r**2) / p_z ) / (1 + (((p_x - x)/p_z)**2))

def grav_sphere(x, rho, r, p_x, p_z, G=6.674e-8):
    return (4./3)*np.pi*G*rho*p_z*r**3 / ( ((p_x - x)**2 + p_z**2)**(3./2) )


# Paramètres intiaux pour calculer la réponse des corps simples
rho_1 = 4.78
R_1 = 12.8*100
PosX_1 = 75.*100
PosZ_1 = 19.*100

rho_2 = -1.45
R_2 = 16.3*100
PosX_2 = 200.*100
PosZ_2 = 23.*100

rho_3 = 1.26
R_3 = 10.0*100
PosX_3 = 350.*100
PosZ_3 = 21.5*100

rho_4 = 3.02
R_4 = 5.0*100
PosX_4 = 150.*100
PosZ_4 = 11.5*100

rho_5 = -2.67
R_5 = 13.5*100
PosX_5 = 450.*100
PosZ_5 = 15.2*100

# Générer le data synthétique à partir des paramètres initiaux
axeX = np.arange(0,500,5)*100
g_1 = grav_sphere(axeX, rho_1, R_1, PosX_1, PosZ_1)
g_2 = grav_sphere(axeX, rho_2, R_2, PosX_2, PosZ_2)
g_3 = grav_cylindre(axeX, rho_3, R_3, PosX_3, PosZ_3)
g_4 = grav_cylindre(axeX, rho_4, R_4, PosX_4, PosZ_4)
g_5 = grav_sphere(axeX, rho_5, R_5, PosX_5, PosZ_5)
g_data = g_1 + g_2 + g_3 + g_4 + g_5

# Ajouter un bruit Gaussien de 2%
g_data += np.random.normal(0,0.02*max(abs(g_data)),size=len(g_data)) 
np.savetxt("Donnees_gravite_TP03_demo.csv", np.vstack((axeX, g_data)).T, delimiter=',', header='Position (m), Gravite (mGal)')

class MainApplication:
    def __init__(self, master):
        self.master = master
        # Séparer les colonnes
        # Construire l'interface
        self.make_frames()
        self.make_buttons()
        self.build_menu()
        self.empty_lists()
        
    # Générer des listes vides pour entreposer les paramètres choisis
    def empty_lists(self):
        self.param1 = []
        self.param2 = []
        self.param3 = []
        self.param4 = []
        self.param5 = []
        self.param6 = []
        self.rms_list = []
        try:
            self.but_reset.config(state=tk.DISABLED)
            self.reponse.set_ydata(np.zeros(len(self.axeX)))
            self.fig_data.canvas.draw()
            self.rms_line.set_ydata(0)
            self.rms_line.set_xdata(0)
            self.fig_rms.canvas.draw()
        except:
            pass
        
    def get_data(self):
        # Importer les donnees
        data = np.loadtxt(self.open_files[0], delimiter=',', skiprows=1)
        self.axeX = data[:,0]
        self.g = data[:,1]  
    
    def plot_inversion_progress(self):
        best_g_model = grav_sphere(axeX, self.param1[-1], R_1, PosX_1, PosZ_1)\
                      + grav_sphere(axeX, rho_2, self.param2[-1], PosX_2, PosZ_2)\
                      + grav_cylindre(axeX, rho_3, R_3, PosX_3, self.param3[-1])\
                      + grav_cylindre(axeX, rho_4, self.param4[-1], PosX_4, PosZ_4)\
                      + grav_sphere(axeX, rho_5, R_5, PosX_5, self.param5[-1])
        self.reponse.set_ydata(1000*best_g_model)
        self.fig_data.canvas.draw() # Retrace le graphique

    def plot_rms_progress(self):
        self.rms_line.set_ydata(self.rms_list)
        self.rms_line.set_xdata(range(len(self.rms_list)))
        self.ax_rms.set_xlim([0, len(self.rms_list)])
        self.ax_rms.set_ylim([0, max(self.rms_list)])
        self.ax_rms.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        self.fig_rms.canvas.draw()

    def MC_inversion(self):
        self.but_reset.config(state=tk.DISABLED)
        # Tester N hypothèses et calculer la fonction objectif 
        for i in range(self.iterations.get()):
            if i % (self.iterations.get()/100) == 0:
                self.it_left.set(self.iterations.get() - i)
                self.fig_rms.canvas.draw()
            # Générer des paramètres de façon aléatoire
            rho_mod_1 = np.random.uniform(0,10)
            R_mod_2 = np.random.uniform(0,23)*100
            PosZ_mod_3 = np.random.uniform(10,30)*100 
            R_mod_4 = np.random.uniform(0,23)*100
            PosZ_mod_5 = np.random.uniform(10,30)*100
            
            # Calculer le modèle proposé
            g_model = grav_sphere(axeX, rho_mod_1, R_1, PosX_1, PosZ_1)\
                     + grav_sphere(axeX, rho_2, R_mod_2, PosX_2, PosZ_2)\
                     + grav_cylindre(axeX, rho_3, R_3, PosX_3, PosZ_mod_3)\
                     + grav_cylindre(axeX, rho_4, R_mod_4, PosX_4, PosZ_4)\
                     + grav_sphere(axeX, rho_5, R_5, PosX_5, PosZ_mod_5)
                     
            # La fonction objectif (Root Mean Square Error)
            RMS = np.sqrt(((g_model - self.g) ** 2).mean()) 
            # Entreposer les paramètres si c'est la première itération ou si la 
            # nouvelle hypothèse est plus probable que la précédente
            if (i == 0) or (RMS < self.rms_list[-1]):
                self.it_left.set(self.iterations.get() - i)
                self.rms_list.append(RMS)
                self.param1.append(rho_mod_1)
                self.param2.append(R_mod_2)
                self.param3.append(PosZ_mod_3)
                self.param4.append(R_mod_4)
                self.param5.append(PosZ_mod_5)
                self.plot_inversion_progress() 
                self.plot_rms_progress()
                if self.ralenti.get():
                    time.sleep(1)
        self.but_reset.config(state=tk.ACTIVE)
        self.it_left.set("-")
    def plot_rms(self):
        self.fig_rms, self.ax_rms = plt.subplots(figsize=(6,3))
        self.rms_line, = self.ax_rms.plot(self.rms_list, 'bo-')
        plt.xlabel("# Iteration")
        plt.ylabel("RMS (mGal)")
        plt.close()
        
    def plot_data(self):
        self.fig_data, ax_data = plt.subplots(figsize=(6,3))
        ax_data.plot(axeX/100, 1000*self.g, 'k.')
        self.reponse, = ax_data.plot(axeX/100, np.zeros(len(self.axeX)), 'r-')
        ax_data.set_ylim([-1, 1])
#        ax_data.set_xlim([0, 800])
        plt.xlabel("Position (m)")
        plt.ylabel("Gravite (mGal)")
        plt.close()
        
    def make_frames(self):
        #==============================================================================
        # Build GUI by calling the main GUI functions
        self.frame_bout = tk.LabelFrame(self.master, text="Inversion", font=("TkDefaultFont", 12, "bold"))
        self.frame_bout.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,0), pady=10)
        self.frame_data = tk.LabelFrame(self.master, text="Reponse gravimetrique", font=("TkDefaultFont", 12, "bold"))
        self.frame_data.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.frame_rms = tk.LabelFrame(self.master, text="Fonction objectif", font=("TkDefaultFont", 12, "bold"))
        self.frame_rms.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        
    def make_buttons(self):
        self.but_run = tk.Button(self.frame_bout, text="GO", command=lambda: self.MC_inversion())
        self.but_run.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.but_reset = tk.Button(self.frame_bout, text="Reset", command=lambda: self.empty_lists())
        self.but_reset.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.iterations = tk.IntVar()
        self.iterations.set(10000)
        tk.Label(self.frame_bout, text="Nb iterations:").grid(row=3, column=0, sticky=tk.W+tk.N, padx=10, pady=0)
        tk.Entry(self.frame_bout, textvariable=self.iterations).grid(row=4, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=(0,10))
        self.ralenti = tk.BooleanVar()
        tk.Checkbutton(self.frame_bout, text="Ralenti", variable=self.ralenti).grid(row=5, column=0, sticky=tk.W+tk.E+tk.N, padx=10, pady=10)
        self.ralenti.set(True)
        self.it_left = tk.StringVar()
        self.it_left.set("-")
        tk.Label(self.frame_bout, textvariable=self.it_left).grid(row=6, column=0, sticky=tk.W+tk.N, padx=10, pady=10)

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
        canvas_rms = FigureCanvasTkAgg(self.fig_rms, master=self.frame_rms)
        canvas_rms.get_tk_widget().grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        canvas_rms.show()
        # Ajoute une barre d'outils
#        topo_toolbar_frame = tk.Frame(self.frame_topo)
#        topo_toolbar_frame.grid(row=0,column=0,columnspan=2, sticky=tk.W)
#        NavigationToolbar2TkAgg(canvas_topo, topo_toolbar_frame)

    def get_file_list(self):
        # Va chercher une liste de fichier à ouvrir
        files = tkFileDialog.askopenfilenames(parent=self.master,title='Choose a file')
        self.open_files = sorted(list(files))
        self.get_data()
        self.plot_data()
        self.plot_rms()
        self.draw_canvas()

#==============================================================================
# Main function
#==============================================================================
def main():
    root = tk.Tk()
    root.wm_title("Démo inversion géophysique")
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