
from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Analytics.SummaryStatistics import SummaryStatistics
from Enums.OrderType import OrderType

import numpy as np


class EfficientPrice:

    def __init__(self, limit_order_book_updater):
        self.limit_order_book_updater = limit_order_book_updater
        self.summary_stats = SummaryStatistics(limit_order_book_updater.messages)

    def calculate_theta(self, k=150, start_time=34200, end_time=34340):
        # calculate mu
        # then h(y_t)
        # then invert h(y_t)
        T = end_time - start_time
        n = self.summary_stats.number_order_buy_sell_time(OrderType.Submission, start_time, end_time)
        mu = n / T
        theta = list()
        for i in range(1, k + 1):
            orders = self.summary_stats.number_order_buy_sell_time(OrderType.Submission, start_time + (i - 1) * T / k,
                                                start_time + (i - 1) * T / k + (6 / 7.15))
            theta.append(orders / (n / k))

        theta = np.sort(theta)

        return theta

    def calculate_efficient_price(self, theta, bid_price):
        spread = list()

        for i in range(1, 140):
            cont = list(filter(lambda x: x <= i, theta))
            spread.append(np.sum(cont) / 150)

        eff_price = [bid_price[i]+spread[0] for i in range(0, len(bid_price))]

        return eff_price, spread