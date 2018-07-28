
import numpy as np
from Interfaces.IVolatility import IVolatility


class Volatility(IVolatility):

    def __init__(self, time_series):
        self.time_series = time_series

    def calculate_standard_deviation(self):
        return np.std(self.time_series)

    def calculate_volatility(self):
        return np.std(self.time_series)
