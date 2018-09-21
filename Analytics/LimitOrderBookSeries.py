
import pandas as pd


class LimitOrderBookSeries(pd.Series):

    def __init__(self, values, idx):
        pd.Series.__init__(self, values, idx)

    def remove_outliers(self, replacement_method='mid_point'):
        # use mid point, remove, use previous value or next value
        None

    def calculate_volatility(self):
        import numpy as np
        return np.std(self.series.tolist())
