
import pandas as pd


class LimitOrderBookSeries(pd.Series):

    def __init__(self, values):
        super(LimitOrderBookSeries, self).__init__(data=values)

    def remove_outliers(self, replacement_method='mid_point'):
        # use mid point, remove, use previous value or next value
        None

    def calculate_volatility(self, window):
        None