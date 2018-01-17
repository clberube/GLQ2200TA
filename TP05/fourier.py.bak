# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:04:32 2016

@author: Charles
"""

import numpy as np

import matplotlib.pyplot as plt


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

t = np.arange(256)

noise = 5e-1 * (0.5-np.random.rand(len(t)))
#noise = 0

#func = 10*np.sin(np.pi*t/350.) + noise + 5*gaussian(t, 300, 5)

func = noise + 10*np.sin(2*np.pi*t/250.) + 5*gaussian(t, 150, 10)

#func = 1*np.sin(2*np.pi*t/5) + 1*np.sin(2*np.pi*t/20)

sp = 1*np.fft.fft(func)

#sp = np.zeros(len(t), dtype=complex)
#for k in range(len(func)):
#    exp = func*np.exp(-2j*np.pi*t*k/len(t))
#    sp[k] = np.sum(exp)

#freq = np.fft.fftfreq(t.shape[-1])
freq = np.hstack((np.linspace(0,0.5,len(t)/2),np.linspace(-0.5,0,len(t)/2)))
#freq = 1.*np.arange(0, len(t))/len(t)

#freq = np.linspace(0,len(t),len(t))/len(t)


#freq = t / max(t)


sp_cut = sp.copy()


fig1 = plt.figure()
plt.semilogy(np.sort(freq), abs(sp[freq.argsort()]),lw=1)
plt.fill_between(np.sort(freq), 1e-3, abs(sp[freq.argsort()]), alpha=0.1)
plt.xlabel(u"Fréquence ($m^{-1}$)")
plt.ylabel("Amplitude (mGal)")
plt.xlim([min(freq), max(freq)])
fig1.savefig("Amplitude.png", dpi=200)


fig2 = plt.figure()
plt.plot(freq, np.angle(sp),lw=1)
plt.xlabel(u"Fréquence ($m^{-1}$)")
plt.ylabel("Phase")
fig2.savefig("Phase.png", dpi=200)

#sp_cut[(freq>0.004)&(freq<0.996)] = 0
#sp_cut[(freq>-0.496)&(freq<0.496)] = 0

sp_cut[abs(freq)>0.004] = 0

inv_fft = np.fft.ifft(sp_cut)

#inv_fft = np.zeros(len(t))
#for m in range(len(sp)):
#    exp = sp*np.exp(2j*np.pi*t*m/len(t))
#    inv_fft[m] = (1./len(t)) * np.sum(exp)


fig = plt.figure()
plt.plot(t, func, "k", lw=1, label=u"Profil brut")
plt.plot(t, inv_fft, "b", lw=1.5, label=u"Prolongement vers le haut")
plt.plot(t, func-inv_fft, "r", lw=2, label=u"Anomalie résiduelle")
leg = plt.legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(3)
plt.ylabel(u"Gravité (mGal)")
plt.xlabel(u"Distance (m)")
plt.show()
fig.savefig("Fourier.png", dpi=200)

data = np.vstack((t, func)).T
np.savetxt("profilgravi.dat", data, delimiter=",")