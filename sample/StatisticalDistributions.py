"""
    Aim:
        statistical distributions for data

"""

import numpy as np
from numpy import cos, sin, tan, pi, log, sign, exp, sqrt

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']

class StatisticalDistributions:
    
    distributionList = []
    
    def __init__(self,distributionName):
        self.distributionList.append(distributionName)
    
    def GetDistributionList(self):
        return self.distributionList
        
    def AddDistribution(self,distName):
        self.distributionList.append(distName)
    
    def RemoveDistribution(self,distName):
        newList = []
        
        for dist in self.distributionList:
            if dist == distName:
                continue
            newList.append(dist)
        
        self.distributionList = newList


class LevyStable:
    # any variable I define here is a static variable
    def __init__(self, alpha, beta, c, mu):
        self.alpha = alpha
        self.beta = beta
        self.c = c
        self.mu = mu

    def __str__(self):
        return str("returns the characteristic function")

    def _phi(self, t):
        if self.alpha == 1:
            return (-2.0 / np.pi) * np.log(t)
        else:
            return np.tan(np.pi * self.alpha / 2.0)

    def PhiCont(self, t):
        if self.alpha == 1:
            return -2.0 / pi * log(abs(self.c * t))
        else:
            return (abs(self.c * t) ** (1 - self.alpha) - 1) * tan(pi * self.alpha / 2)

    def CharFunction(self, t):  # characteristic function

        if type(t) == float:
            return np.exp(
                t * self.mu - (np.abs(self.c * t) ** self.alpha) * (1 - np.sign(t) * self.beta * self._phi(t)))
        else:
            size = len(t)
            output = np.zeros(size)  # 1-d array

            for i in range(0, size):
                output[i] = np.exp(t[i] * self.mu - (np.abs(self.c * t[i]) ** self.alpha) * (
                1 - np.sign(t[i]) * self.beta * self._phi(t[i])))

            return output

    def EulerIdentity(self, t):
        # this is the case when alpha =1
        if type(t) == np.float64:
            rho = (self.beta * sign(t) * 2.0 / pi * log(abs(self.c * t)) - t * self.mu) * abs(self.c * t)
            return complex(cos(rho), sin(rho))
        else:
            size = np.size(t)
            output = np.zeros(size, dtype=np.complex)

            for i in range(0, size):
                rho = (self.beta * sign(t[i]) * 2.0 / pi * log(abs(self.c * t[i])) - t[i] * self.mu) * abs(
                    self.c * t[i])
                output[0, i] = cos(rho) + sin(rho) * 1j

    def SimplifiedChar(self, x):

        return exp(
            -self.c * abs(x) * (1 + 1j * self.beta * (2.0 / pi) * sign(x)) * log(self.c * abs(x)) + 1j * self.mu * x)


class GumbelDist:
    _euler_mascheroni = 0.5772

    def __init__(self, mu, std_dev):
        self.beta = sqrt(6 * std_dev ** 2 / pi ** 2)
        self.alpha = mu + self._euler_mascheroni * self.beta

    def pdf(self, x):
        z = (x - self.alpha) / self.beta
        return (1 / self.beta) * exp(-(z + exp(-z)))

    def cdf(self, x):
        z = (x - self.alpha) / self.beta
        return exp(-exp(-z))

    def fit_pdf(self, returns_to_fit):
        # check if average and std dev of returns to fit matches the implied beta and alpha values
        # for now take as given
        if type(returns_to_fit) == list:
            returns_to_fit.sort()
            output = list([])
            for i in range(0, len(returns_to_fit)):
                output.append(self.pdf(returns_to_fit[i]))
            return output
        None
