from unittest import TestCase
from scipy.stats import norm
import numpy as np


class TestGaussianDistribution(TestCase):
    def test_fit_data(self):
        # arrange
        location = 0.0
        scale = 1.0
        time_series = norm.rvs(loc=location, scale=scale, size=10000)
        tol = 10e-2

        # act
        parameters = norm.fit(time_series)

        # assert
        self.assertTrue(np.abs(location-parameters[0]) < tol)
        self.assertTrue(np.abs(scale-parameters[1]) < tol)
