"""
Make this class a singleton class

Explain, why this method has its own class

"""


class OrderBookImbalance:

    def __init__(self):
        pass

    @staticmethod
    def calculate_imbalance(buy_time_series, sell_time_series):
        """
        :param buy_time_series:
        :param sell_time_series:
        :return:
        """
        if len(buy_time_series) != len(sell_time_series):
            raise ValueError('Time series must be of the same length')

        imbalance = [buy_time_series[i]/sell_time_series[i] for i in range(0, len(buy_time_series))]
        return imbalance
