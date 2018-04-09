from unittest import TestCase
import numpy as np
from scipy.stats import t


class TestStudentTDistribution(TestCase):
    def test_fit_data(self):
        # arrange
        df = 2
        time_series = t.rvs(df, size=10000)
        tol = 10e-2

        # act
        parameters = t.fit(time_series)

        # assert
        self.assertTrue(np.abs(parameters[0] - df) < tol)
