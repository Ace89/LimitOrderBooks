
import numpy as np


class StatisticalTests:

    def __init__(self):
        None

    @staticmethod
    def sum_squared_errors(y, y_hat):
        """
        :param y:
        :param y_hat:
        :return:
        """
        return np.sum((y - y_hat) ** 2)

    @staticmethod
    def chow_test(x, y, n1, n2, k=2):
        """
        :param x:
        :param y:
        :param n1:
        :param n2:
        :param k:
        :return:
        """
        from Analytics.LinearRegression import LinearRegression
        linear_model = LinearRegression()
        x1 = x[0:n1]
        x2 = x[n1:(n1 + n2)]
        y1 = y[0:n1]
        y2 = y[n1:(n1 + n2)]
        [a, b] = linear_model.fit_data(x, y)
        [a1, b1] = linear_model.fit_data(x1, y1)
        [a2, b2] = linear_model.fit_data(x2, y2)

        s_c = StatisticalTests.sum_squared_errors(y, a+b*x)
        s_1 = StatisticalTests.sum_squared_errors(y1, a1+b1*x1)
        s_2 = StatisticalTests.sum_squared_errors(y2, a2+b2*x2)

        return ((s_c - (s_1 + s_2)) / k) / ((s_1 + s_2) / (n1 + n2 - 2 * k))

    @staticmethod
    def hurst_exponent(time_series, lags):
        """
        :param time_series:
        :param lags:
        :return:
        """
        tau = [np.sqrt(np.std(np.subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]
        m = np.polyfit(np.log(lags), np.log(tau), 1)
        hurst = m[0] * 2.0
        return hurst