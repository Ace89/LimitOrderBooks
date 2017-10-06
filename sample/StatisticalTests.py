"""
Outline statistical tests such as
-> Chow test
-> If variance of two populations is equal
-> Calculate the hurst exponent
"""

import numpy as np

"""
Chow Test:

Suppose data is modeled aas
    y(t) = a + b x1(t) + c x2(t) + e
    
Split the data into two groups
    y(t) = a1 + b1 x1(t) + c1 x2(t) + e
and
    y(t) = a2 + b2 x1(t) + c2 x2(t) + e

Nul hypothesis is that a1=a2, b1=b2, c1=c2

Test statistic = (Sc - (S1 + S2))/k / (S1 + S2)/(N1 + N2 - 2*k)

Sc is the sum of squared residuals from the combined data
N1 is the number of observations in the first group
k is the total number of parameters
"""


def linear_regression(x, y):
    x_bar = np.average(x)
    y_bar = np.average(y)
    s_xy = np.sum((x-x_bar)*(y-y_bar))
    s_xx = np.sum((x-x_bar)**2)
    b_hat = s_xy/s_xx
    a = y_bar - b_hat*x_bar
    return [a, b_hat]


def sum_squared_errors(parameters, x, y):
    y_hat = parameters[0] + parameters[1]*x
    # for bottom line to run, y has to be a numpy array and not a list
    return np.sum((y-y_hat)**2)


def chow_test(x, y, n1, n2, k=2):
    # test stat follows a F distribution
    x1 = x[0:n1]
    x2 = x[n1:(n1+n2)]
    y1 = y[0:n1]
    y2 = y[n1:(n1+n2)]
    [a, b] = linear_regression(x, y)
    [a1, b1] = linear_regression(x1, y1)
    [a2, b2] = linear_regression(x2, y2)

    s_c = sum_squared_errors([a, b], x, y)
    s_1 = sum_squared_errors([a1, b1], x1, y1)
    s_2 = sum_squared_errors([a2, b2], x2, y2)

    return ((s_c - (s_1 + s_2)) / k) / ((s_1 + s_2)/(n1 + n2 - 2*k))


def hurst_exponent(time_series, lags):
    tau = [np.sqrt(np.std(np.subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]
    m = np.polyfit(np.log(lags), np.log(tau), 1)
    hurst = m[0] * 2.0
    return hurst