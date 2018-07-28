
"""
Make this class a singleton class as it does not need to hold state

why is this a class on its own i.e. will their be other methods which will be added to this class

why choose to eliminate outlier, can you also replace outlier with another value i.e. an average

Why have I not used a factory to create a data cleaning class, instead why have I decided to extend this class with new methods.

I could have done the same with the volatility class

"""


class DataCleaning:

    def __init__(self):
        None

    @staticmethod
    def remove_outliers(time_series):
        """
        :param time_series: time series
        :return: time series with outliers removed
        """
        import numpy as np
        std_deviation = np.std(time_series)
        lower_bound = -1.50 * std_deviation
        upper_bound = 1.50 * std_deviation

        filtered_data = []

        for val in time_series:
            if lower_bound <= val <= upper_bound:
                filtered_data.append(val)

        return filtered_data
