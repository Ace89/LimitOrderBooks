from unittest import TestCase
import numpy as np
from scipy.stats import norm
from Analytics.GarchModel import GarchModel


"""
X(t) = sigma(t)Z(t)

sigma(t)**2 = alpha + omega*X(t-1) + beta*sigma(t-1)

"""


class TestGarchModel(TestCase):
    def test_fit_data(self):
        # arrange
        alpha = 0.5
        omega = 1.0
        beta = 1.0
        size = 100
        X_0 = 2
        Vol_0 = 0.05
        X = []
        Vol = []
        X.append(X_0)
        Vol.append(Vol_0)
        Z = norm.rvs(size=size)
        for i in range(1, size):
            Vol.append(alpha + omega*X[i-1]+beta*np.sqrt(Vol[i-1]))
            X.append(Vol[i]*Z[i])

        model = GarchModel()
        # act
        parameters = model.calib_data(X)

        # assert
        self.assertTrue(parameters[0], alpha)
        self.assertTrue(parameters[1], beta)
        self.assertTrue(parameters[2], omega)
