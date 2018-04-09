from unittest import TestCase
from sklearn import linear_model
import numpy as np


class TestLinearModel(TestCase):
    def test_fit_data(self):
        # arrange
        regr = linear_model.LinearRegression()
        size = 100
        train_vals = np.linspace(-1.0, 1.0, size)
        alpha = 0.5
        beta = 1
        train_output = alpha + beta*train_vals

        # act
        regr.fit(train_vals.reshape(-1, 1), train_output.reshape(-1, 1))

        # assert
        self.assertTrue(regr.intercept_[0], alpha)
        self.assertTrue(regr.coef_[0], beta)
