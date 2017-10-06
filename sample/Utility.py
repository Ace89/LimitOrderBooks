"""
    Aim:
        Utility module
        contains functions that will come in handy
"""

from scipy.stats import pearsonr
from scipy.optimize import fmin_slsqp
import numpy as np
from numpy import log, pi


def interpolate(x, y, _x):
    # linear interpolations
    # check bounds
    index = 0
    while x[index] < _x:
        index += 1

    w1 = (_x - x[index]) / (x[index + 1] - x[index])
    w2 = (x[index + 1] - _x) / (x[index + 1] - x[index])

    return w2 * y[index] + w1 * y[index + 1]


def auto_correlation(window_length, lag, time_series):
    auto_correls = []
    for i in range(window_length + 1, len(time_series)):
        temp_series_A = []
        temp_series_B = []
        for j in range(0, window_length):
            temp_series_A.append(time_series[i - j])
            temp_series_B.append(time_series[i - j - lag])
        tmp = pearsonr(temp_series_A, temp_series_B)
        auto_correls.append(tmp[0])
    return auto_correls


def auto_regressive_constraint(parameters, data, vols, out=None):
    c = parameters[0]
    phi = parameters[1]
    sigma = parameters[2]
    return 1 - np.abs(phi)


def auto_regressive_likelihood(parameters, data, vols, out=None):
    c = parameters[0]
    phi = parameters[1]
    sigma = parameters[2]
    size = len(data)
    eps = np.zeros((size,1))
    eps[0] = data[0]
    for i in range(1,size):
        eps[i] = phi*data[i-1] + c

    logliks = 0.5*(log(2.0*pi) + log(sigma) + eps**2/sigma)
    loglik = np.sum(logliks)

    if out is None:
        return loglik
    else:
        return loglik, logliks, eps


def calib_auto_regressive(data):
    starting_vals = np.array([0.3, 0.3, 0.3])
    bounds = [(-10.0 * np.average(data), 10.0*np.average(data)), (-1.0, 1.0), (0.0, 4.0)]
    vols = np.zeros((len(data),1))
    args = (data,vols)
    estimates = fmin_slsqp(auto_regressive_likelihood, starting_vals, f_ieqcons=auto_regressive_constraint, bounds=bounds, args=args)
    return estimates


def arma_model(target_series, noise_series, variance, phi=0.5, theta=0.5):
    # X(t) = phi*X(t-1) + Z(t) + theta*Z(t-1)
    # Z(t) ~ N(0, variance)
    # params to calibrate: phi(0), phi1, theta1, variance
    return target_series[-1]*phi + np.random.randn()*np.sqrt(variance) + theta*noise_series[-1]


def arma_likelihood(parameters, data, vols, out=None):
    phi = parameters[0]
    theta = parameters[1]
    sigma = parameters[2]
    size = len(data)
    eps = np.zeros((size, 1))
    eps[0] = data[0]
    for i in range(1, size):
        eps[i] = phi*eps[i-1] + theta*data[i-1] + data[i]

    logliks = 0.5*(log(2.0*pi) + log(sigma) + eps**2/sigma)
    loglik = np.sum(logliks)

    if out is None:
        return loglik
    else:
        return loglik, logliks, eps


def arma_constraint(parameters, data, vols, out=None):
    phi = parameters[0]
    theta = parameters[1]
    sigma = parameters[2]
    return 1 - np.abs(phi)


def calib_arma(data):
    starting_vals = np.array([0.3, 0.3, 0.3])
    bounds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    vols = np.zeros((len(data),1))
    args = (data, vols)
    estimates = fmin_slsqp(arma_likelihood, starting_vals, f_ieqcons=arma_constraint, bounds=bounds, args=args)
    return estimates


def garch_likelihood(parameters, data, vol, out=None):
    mu = parameters[0]
    omega = parameters[1]
    alpha = parameters[2]
    beta = parameters[3]
    eps = data-mu
    for i in range(1, len(data)):
        vol[i] = omega + alpha*eps[i-1]**2 + beta*vol[i-1]

    logliks = 0.5*(log(2.0*pi) + log(vol) + eps**2/vol)
    loglik = np.sum(logliks)

    if out is None:
        return loglik
    else:
        return loglik, logliks, vol


def garch_constraint(parameters, data, vol, out=None):
    # omega = parameters[0]
    alpha = parameters[1]
    beta = parameters[2]

    return 1-alpha-beta


def calib_garch(data):
    starting_vals = np.array([np.average(data), 0.2, 0.3, 0.9])
    bounds = [(-10*np.average(data), 10*np.average(data)), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    vol = np.repeat(np.var(data), len(data))
    args = (data, vol)
    estimates = fmin_slsqp(garch_likelihood, starting_vals, f_ieqcons=garch_constraint, bounds=bounds, args=args)
    return estimates
