
from Interfaces.INonLinearModel import INonLinearModel
from scipy.optimize import fmin_slsqp
import numpy as np


class GarchModel(INonLinearModel):

    def __init__(self):
        None

    def fit_data(self, data):
        return self.calib_data(data)

    @staticmethod
    def garch_constraint(parameters, data, vol, out=None):
        # omega = parameters[0]
        alpha = parameters[1]
        beta = parameters[2]

        return 1 - alpha - beta

    @staticmethod
    def garch_likelihood(parameters, data, vol, out=None):
        mu = parameters[0]
        omega = parameters[1]
        alpha = parameters[2]
        beta = parameters[3]
        eps = data - mu
        for i in range(1, len(data)):
            vol[i] = omega + alpha * eps[i - 1] ** 2 + beta * vol[i - 1]

        logliks = 0.5 * (np.log(2.0 * np.pi) + np.log(vol) + eps ** 2 / vol)
        loglik = np.sum(logliks)

        if out is None:
            return loglik
        else:
            return loglik, logliks, vol

    def calib_data(self, data):
        starting_vals = np.array([np.average(data), 0.2, 0.3, 0.9])
        bounds = [(-10 * np.average(data), 10 * np.average(data)), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
        vol = np.repeat(np.var(data), len(data))
        args = (data, vol)
        estimates = fmin_slsqp(self.garch_likelihood, starting_vals, f_ieqcons=self.garch_constraint, bounds=bounds, args=args)
        return estimates
