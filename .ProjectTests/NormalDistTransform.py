"""
    Aim:
        Fit distributions to data using characteristic functions
"""

import numpy as np
from numpy import exp, pi
from scipy.stats import norm
import matplotlib.pyplot as plt

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']


class Celsius:  # decorator example
    
    def __init__(self, temperature=0):
        self._temperature = temperature
        
    @property
    def temperature(self):
        print("Getting Value")
        return self._temperature
        
    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("")
        print("Setting Value")
        self._temperature = value


def CharFunction(u, mu, vol):
    return exp(0.5*u**2*vol**5-1j*u*mu)


def FittedCdf(x, mu, vol):
    cont = 0.0
    lower_bound = 0.0
    upper_bound = 0.80
    steps = 1000
    h = (upper_bound-lower_bound)/steps
    trapz = np.zeros((steps,), dtype=complex)

    for i in range(1, steps):
        u = i*(upper_bound/steps)
        trapz[i] = (exp(1j*u*x)*CharFunction(-u,mu,vol)-exp(-1j*u*x)*CharFunction(u,mu,vol))/(1j*u)
    
    for i in range(1, steps):
        cont += (trapz[i-1]+trapz[i])*0.50*h
    
    return 0.5+1.0/(2.0*pi)*cont.real

if __name__ == '__main__':    
    mu = 0.0
    vol = 1.0
    size = 100
    t = np.arange(size)
    x = np.linspace(-5.0, 5.0, size)
    
    fittedPdf = np.zeros((size,))
    actualPdf = np.zeros((size,))

    for i in range(0, size):
        fittedPdf[i] = FittedCdf(x[i],mu,vol)
        actualPdf[i] = norm.cdf(x[i])
    
    plt.plot(t, fittedPdf, 'b-', t, actualPdf, 'r--')
    plt.show()

    [samples, weights] = np.polynomial.hermite.hermgauss(8)
    gauss_cdf = 0.0

    for i in range(0, len(samples)):
        gauss_cdf += norm.pdf(samples[i])*weights[i]

    print("Normal cdf: " + str(gauss_cdf))
