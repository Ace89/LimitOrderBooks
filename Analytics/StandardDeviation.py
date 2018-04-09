
from Interfaces.IVolatility import IVolatility
import numpy as np


class StandardDeviation(IVolatility):

    def __init__(self, time_series):
        self.time_series = time_series

    def calculate_volatility(self):
        return np.std(self.time_series)
