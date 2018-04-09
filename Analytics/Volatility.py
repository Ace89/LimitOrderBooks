
import numpy as np


class Volatility:

    def __init__(self, time_series):
        self.time_series = time_series

    def calculate_standard_deviation(self):
        return np.std(self.time_series)