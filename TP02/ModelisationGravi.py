# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 20:44:22 2015

@author: Charles
"""
from __future__ import division

from future import standard_library
standard_library.install_aliases()
from builtins import range
from past.utils import old_div
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import numpy as np
from platform import system

size = 10
window_font = "TkDefaultFont %s"%size
fontz = {"bold": ("TkDefaultFont", size, "bold"),
         "normal": ("TkDefaultFont", size, "normal"),
         "italic": ("TkDefaultFont", size, "italic")}

colors = ["red", "blue", "darkgreen"]

G = 6.67408e-11
phis=np.arange(0,6.28,0.01)
x = np.linspace(-100,100)
def xy(r,phi,shift,depth):
  return r*np.cos(phi)+shift, r*np.sin(phi)+depth

solution = [[15, 30, 50],        # Z
            [-60, 54, -1],       # X
            [2900, 3500, 3200],  # d
            [7, 7, 10],          # R
]

#==============================================================================
# Main window frames - geometry - font - labels
def main_frames():
    global frame_sliders, frame_plot
    frame_sliders = tk.LabelFrame(root, text="Parametres du modele", font=fontz["bold"])
    frame_sliders.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N, padx=(10,0), pady=10)
    frame_plot = tk.LabelFrame(root, text="Reponse gravimetrique", font=fontz["bold"])
    frame_plot.grid(row=0, column=1, rowspan=2,sticky=tk.W+tk.E+tk.N, padx=10, pady=10)

def make_data(n_sphe):
    depth = solution[0]
    shift = solution[1]
    density = solution[2]
    radius = solution[3]
    g = np.zeros(len(x))
    for n in range(n_sphe):
        r = np.sqrt((x-shift[n])**2 + depth[n]**2)
        noise = np.random.rand(len(x))
        g += 0.1*(0.5-noise) + 1e5*depth[n] * G * density[n]*((old_div(4,3))*np.pi*radius[n]**3) / ((x-shift[n])**2 + depth[n]**2) **(old_div(3,2))
    return g

def number_spheres(n_ini):
    frame_opt = tk.Frame(frame_sliders)
    frame_opt.grid(row=0, column=2)
    tk.Label(frame_opt, text="Nb spheres: ").grid(row=0, column=0)
    n_sphe = tk.IntVar()
    n_sphe.set(n_ini)
    tk.Entry(frame_opt, textvariable=n_sphe, width=10).grid(row=0, column=1)
    tk.Button(frame_opt, text="OK", command=lambda: draw_sliders(n_sphe)).grid(row=0, column=2)
    return n_sphe.get()

def draw_sliders(n_sphe):
    try: frame_sliders.destroy(), frame_plot.destroy()
    except: pass
    main_frames()
    sliders(n_sphe.get())
    plot_model(n_sphe.get())
    plot_frame()
    number_spheres(n_sphe.get())


def sliders(n_sphe):
    global grav_vars, n
    ct = 1
    grav_vars = {}
    for n in range(n_sphe):
        tk.Label(frame_sliders, text="Sphere %i"%(n+1), font=fontz["bold"], fg=colors[n]).grid(row=ct, column=0, sticky=tk.W)
        grav_vars[n] = [("Profondeur (m)"       , tk.DoubleVar(), 15, 85, 10*n+50, 1),
                        ("X (m)"  , tk.DoubleVar(), -80, 80, (10*n+7), 1),
                        ("Densité (kg/m^3)", tk.DoubleVar(), 0, 3500, 2700+n*200, 50),
                        ("Rayon (m)"      , tk.DoubleVar(), 1, 14, 11+n, 0.1),
]
        ct+=1
        for i, (k, v, f, t, s, r) in enumerate(grav_vars[n]):
            v.set(s)
            tk.Label(frame_sliders, text=k).grid(row=ct, column=1, sticky=tk.W)
#            print n
            if n == 0:
                tk.Scale(frame_sliders, variable=v, width=15, length=200, from_=f, to=t, resolution=r, command=update_plot0, font=fontz["normal"], orient=tk.HORIZONTAL).grid(row=ct, column=2, sticky=tk.E, padx=10)
            if n == 1:
                tk.Scale(frame_sliders, variable=v, width=15, length=200, from_=f, to=t, resolution=r, command=update_plot1, font=fontz["normal"], orient=tk.HORIZONTAL).grid(row=ct, column=2, sticky=tk.E, padx=10)
            if n == 2:
                tk.Scale(frame_sliders, variable=v, width=15, length=200, from_=f, to=t, resolution=r, command=update_plot2, font=fontz["normal"], orient=tk.HORIZONTAL).grid(row=ct, column=2, sticky=tk.E, padx=10)
            ct+=1

def compute_model(n):
    depth = grav_vars[n][0][1].get()
    shift = grav_vars[n][1][1].get()
    density = grav_vars[n][2][1].get()
    radius = grav_vars[n][3][1].get()
    r = np.sqrt((x-shift)**2 + depth**2)
    response = 1e5*depth * G * density*((old_div(4,3))*np.pi*radius**3) / ((x-shift)**2 + depth**2)**(old_div(3,2))
    return depth, density, radius, shift, response

def update_plot0(e):
    depth, density, radius, shift, response = compute_model(0)
    curve[0].set_ydata(response)
    sphere[0].set_ydata(xy(radius,phis,shift,-depth)[1])
    sphere[0].set_xdata(xy(radius,phis,shift,-depth)[0])
    sphere[0].set_alpha(old_div((density),grav_vars[0][2][3]))
    total = compute_sum()
    tot_curve.set_ydata(total)
    fig.get_axes()[0].set_ylim([0, 1.3*max(total)])
    fig.canvas.draw()

def update_plot1(e):
    depth, density, radius, shift, response = compute_model(1)
    curve[1].set_ydata(response)
    sphere[1].set_ydata(xy(radius,phis,shift,-depth)[1])
    sphere[1].set_xdata(xy(radius,phis,shift,-depth)[0])
    sphere[1].set_alpha(old_div(density,grav_vars[1][2][3]))
    total = compute_sum()
    tot_curve.set_ydata(total)
    fig.get_axes()[0].set_ylim([0, 1.3*max(total)])
    fig.canvas.draw()

def update_plot2(e):
    depth, density, radius, shift, response = compute_model(2)
    curve[2].set_ydata(response)
    sphere[2].set_ydata(xy(radius,phis,shift,-depth)[1])
    sphere[2].set_xdata(xy(radius,phis,shift,-depth)[0])
    sphere[2].set_alpha(old_div((density),grav_vars[2][2][3]))
    total = compute_sum()
    tot_curve.set_ydata(total)
    fig.get_axes()[0].set_ylim([0, 1.3*max(total)])
    fig.canvas.draw()

def compute_sum():
    try:
        return curve[0].get_ydata()+curve[1].get_ydata()+curve[2].get_ydata()
    except:
        try:
            return curve[0].get_ydata()+curve[1].get_ydata()
        except:
            return curve[0].get_ydata()

def plot_model(n_sphe):
    global curve, sphere, fig, n, tot_curve
    depth, density, radius, shift, response, sphere, curve = {}, {}, {}, {}, {}, {}, {}
    fig, ax = plt.subplots(2,1,figsize=(6,8))
    ax[0].errorbar(x, make_data(n_sphe),(old_div(n_sphe,2))*0.1*np.random.rand(len(x)),None, color='k',ms=5 ,fmt='o', mfc='white', zorder=1, label="Observations")
    for n in range(n_sphe):
        depth[n], density[n], radius[n], shift[n], response[n] = compute_model(n)
        curve[n], = ax[0].plot(x, compute_model(n)[4], c=colors[n],ls='-',lw=2, label="Sphere %i"%(n+1))

        ax[0].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off
#        ax[0].set_ylim([0,None])
        ax[0].set_ylabel("Gravity (mGal)")
        ax[0].grid('off')
        ax[1].plot(x, np.zeros(len(x)), c='gray',ls='-',lw=5)
        ax[1].set_aspect('equal', adjustable='box')
        ax[1].set_ylim([-100, 1])
        ax[1].set_ylabel("Y (m)")
        ax[1].set_xlabel("X (m)")
        sphere[n], = ax[1].plot( *xy(radius[n],phis,shift[n],-depth[n]), c=colors[n],ls='-',lw=5)
#        plt.tight_layout()
    tot_curve, = ax[0].plot(x, compute_sum(), c="k",ls='--',lw=1, label="Total")
    ax[0].legend(loc="best", fontsize=8)
    plt.close("all")

def plot_frame():
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.show()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan = 3, sticky=tk.N+tk.S+tk.E+tk.W)
    toolbar_frame = tk.Frame(frame_plot)
    toolbar_frame.grid(row=1,column=0,columnspan=2, sticky=tk.W)
    NavigationToolbar2TkAgg(canvas, toolbar_frame)

#==============================================================================
# Window start
root = tk.Tk()
root.wm_title("Modelisation gravite 2D")
root.option_add("*Font", window_font)
#==============================================================================
# Build GUI by calling the main GUI functions
main_frames()
n_sphe = number_spheres(1)
sliders(n_sphe)
plot_model(n_sphe)
plot_frame()
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
