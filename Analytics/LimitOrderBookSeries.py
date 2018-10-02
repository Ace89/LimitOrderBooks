
import pandas as pd
import numpy as np


class LimitOrderBookSeries(pd.Series):

    def __init__(self, values, idx):
        pd.Series.__init__(self, values, idx)

    def remove_outliers(self, replacement_method='mid_point'):
        # use mid point, remove, use previous value or next value
        None

    def calculate_volatility(self):
        return np.std(self.series.tolist())
