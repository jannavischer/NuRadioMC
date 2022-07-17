import glob, os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def linear_fit(x, a, b):
    return a * x + b

#measurements are in mV
for file in (glob.glob("rno_g_surface_trigger_measurements/*T-25*")):
    filename = (os.path.split(file)[-1])
    data = np.genfromtxt(file, delimiter=',', skip_header=1)
    xdata = (data[:,0]*1e-3)**2
    ydata = np.abs(data[:,1]*1e-3)
    plt.plot(xdata, ydata, marker='x',label=f'{filename}')
    popt, pcov = curve_fit(linear_fit, xdata, ydata, bounds=(-200,[100,0]))
    print(popt)
    plt.plot(xdata, linear_fit(xdata, *popt), color='k', ls='--', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
    plt.xlabel(r'$V_{in}^2$[$mV^2$]')
    plt.ylabel(r'$V_{out}$[mV]')
    plt.legend()
    #plt.show()
plt.savefig(f'fit_parameter.png')
plt.show()