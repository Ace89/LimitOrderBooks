
import sample.TimeBuckets
from sample.Bucket import Bucket
import numpy as np
from sample.Order import Order, OrderType, Direction, Visibility

__author__ = ''
__project__ = ''
__maintainer__ = ''
__license__ = ''
__version__ = ''
__all__ = ['price_volatility']


class BucketStats:

    @staticmethod
    def __doc__():
        return 'This class is designed to return statistics on time buckets'

    def __init__(self, time_buckets):
        self.time_buckets = time_buckets

    def price_volatility(self):
        """
            In the message data column 2 contains order types, select types 4 and 5
            4 is execution of visible limit orders
            5 is execution of hidden limit orders

            Column 6 contains order direction
            1 is buy order
            -1 is sell order
        """
        buy_prices, sell_prices = self.get_buy_sell_prices()

        buy_rets = []
        sell_rets = []

        for i in range(1, len(buy_prices)):
            buy_rets.append(np.log(buy_prices[i]/buy_prices[i-1]))

        for i in range(1, len(sell_prices)):
            sell_rets.append(np.log(sell_prices[i]/sell_prices[i-1]))

        return np.std(buy_rets), np.std(sell_rets)
