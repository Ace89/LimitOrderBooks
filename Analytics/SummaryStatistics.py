
import numpy as np
from Time.TimeStructure import TimeStructure


class SummaryStatistics:

    def __init__(self, timeStructure):
        self.time_structure = timeStructure.time_structure
        self.time_series = self.create_array()

    def create_array(self):
        """
        :return: a list of price/volume values
        """
        # list of buckets
        time_structure = self.time_structure
        temp_prices = list()

        for bucket in time_structure:
            temp_prices.append(bucket.price)

        return temp_prices

    def calculate_mean(self):
        """
        :return: Returns time series average
        """
        return np.average(self.time_series)

    def calculate_median(self):
        """
        :return: Returns time series median
        """
        return np.median(self.time_series)

    def calculate_percentile(self, percentile):
        """
        :param percentile: Percentile
        :return: Returns time series percentile
        """
        return np.percentile(self.time_series, percentile)

    @staticmethod
    def calculate_book_imbalance(time_structure_buy, time_structure_sell):
        size = len(time_structure_buy)
        if size != len(time_structure_sell):
            raise ValueError('buy and sell time structures should be the same length')

        imbalance = np.zeros(size)

        for i in range(0, size):
            imbalance[i] = time_structure_buy[i].buy_orders / time_structure_sell[i].sell_orders

        return imbalance

    @staticmethod
    def remove_outliers(time_structure):

        if type(time_structure) == TimeStructure:
            time_structure = time_structure.time_structure

        std_deviation = np.std(time_structure)
        lower_bound = -1.50 * std_deviation
        upper_bound = 1.50 * std_deviation

        filtered_data = []

        for val in time_structure:
            if lower_bound <= val <= upper_bound:
                filtered_data.append(val)

        return filtered_data
