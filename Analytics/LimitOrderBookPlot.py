
import matplotlib.pyplot as plt
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection


class LimitOrderBookPlot:

    def __init__(self, summary_stats, order_data):
        self.summary_stats = summary_stats
        self.order_data = order_data

    def plot_submitted_volume(self):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        import numpy as np
        buy_size = self.summary_stats.size_order_buy_sell()
        sell_size = self.summary_stats.size_order_buy_sell(OrderType.Submission, OrderDirection.Sell)

        fig, ax = plt.subplots()
        idx = np.arange(1, 3)

        ax.set_ylabel('Size')

        pb, ps = plt.bar(idx, (np.sum(buy_size), np.sum(sell_size)))
        pb.set_facecolor('r')
        ps.set_facecolor('b')
        ax.set_xticks(idx)
        ax.set_xticklabels(['Buy', 'Sell'])
        ax.set_ylabel('Size')
        ax.set_title('Buy and Sell Order Sizes')
        plt.show()

    def plot_deleted_volume(self):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        import numpy as np
        buy_size = self.summary_stats.size_order_buy_sell(OrderType.Deletion, OrderDirection.Buy)
        sell_size = self.summary_stats.size_order_buy_sell(OrderType.Deletion, OrderDirection.Sell)

        fig, ax = plt.subplots()
        idx = np.arange(1, 3)

        pb, ps = plt.bar(idx, [np.sum(buy_size), np.sum(sell_size)])
        pb.set_facecolor('r')
        ps.set_facecolor('b')
        ax.set_xticks(idx)
        ax.set_xticklabels(['Buy', 'Sell'])
        ax.set_ylabel('Size')
        ax.set_title('Buy and Sell Deleted Sizes')
        plt.show()

    def plot_price_size(self, limit_order_book_series):
        fig, ax = plt.subplots()
        plt.plot(limit_order_book_series.index, limit_order_book_series.tolist())
        ax.set_ylabel('Price $')
        ax.set_title('Bid price')
        plt.show()
