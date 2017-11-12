
import sample.TimeBuckets
from sample.Bucket import Bucket
import numpy as np
from sample.Order import Order, OrderType, Direction, Visibility

__author__ = ''
__project__ = ''
__maintainer__ = ''
__license__ = ''
__version__ = ''
__all__ = ''


class BucketStats:

    @staticmethod
    def __doc__():
        return 'This class is designed to perform stats on time buckets'

    def __init__(self, time_buckets):
        self.time_buckets = time_buckets

    def get_volume_size(self, time_start, time_end, levels):
        # terrible method name
        # check for unique orders, filter
        # zero is the best level

        if self.time_buckets is None:
            raise ValueError('time buckets have not been initialised')

        orders = []
        data_matrix = self.time_buckets.dataFrame.as_matrix()
        size_data = len(data_matrix)
        orderType = OrderType(1)
        visibility = Visibility(1)
        count = 0

        while data_matrix[count, 0] < time_start:
            count += 1

        # get all submission orders
        while count < size_data and data_matrix[count, 0] <= time_end:
            if data_matrix[count, 1] == 1:   # only interested in new submission orders
                direction = Direction(data_matrix[count, 5])
                order = Order(data_matrix[count, 0], direction, data_matrix[count, 4],
                              data_matrix[count, 3], visibility, OrderType.Submission)
                orders.append(order)
            count += 1

        # get submisison order information
        if len(orders) == 0:
            print("no orders")

        # bid/ask_size contains volumes for each price level in levels
        [ask_prices, ask_sizes, sell_orders] = self._get_level_stats(orders, -1, levels)
        [bid_prices, bid_sizes, buy_orders] = self._get_level_stats(orders, 1, levels)
        # go through the list of orders and for each price see how many copies of the same price

        return [ask_prices, ask_sizes, sell_orders, bid_prices, bid_sizes, buy_orders]

    @staticmethod
    def _get_level_stats(orders, bid_ask, levels):
        #  orders is a list of orders
        # bid_ask, is whether you are interested in bid or ask orders
        # levels, how many levels you are interested in

        unique_orders = []
        order_count = 0
        # get unique prices in orders
        for i in range(0, len(orders)):
            if orders[i].direction == Direction(bid_ask):
                order_count += 1
                if orders[i].price not in unique_orders:
                    unique_orders.append(orders[i].price)

        # sort prices by value
        unique_orders.sort()
        # check if size of unique orders is less than levels
        prices = []
        sizes = []

        # get volumes by sorted prices
        for i in range(0, levels):
            price = unique_orders[i]
            size = 0
            for j in range(0, len(orders)):
                if orders[j].price == price:
                    size += orders[j].volume
            prices.append(price)
            sizes.append(size)

        return [prices, sizes, order_count]

    def create_order_book_levels(self, time_start, time_end, num_buckets, levels=3):
        """
        :param levels: order book levels of interest usually 3
        """
        if self.time_buckets is None:
            raise ValueError('time buckets have not been initialised')

        bucket_string = []
        # interval range for each bucket
        intervals = (time_end - time_start) / num_buckets
        bucket_string.append(0)

        for i in range(1, num_buckets+1):
            bucket = Bucket(time_start + (i-1)*intervals, time_start + i*intervals, 0, 0, 0, 0)
            bucket_string.append(bucket)

        for i in range(1, num_buckets+1):
            # count is just to make sure I do not exceed the matrix dimensions
            [ask_prices, ask_sizes, sell_orders, bid_prices,bid_sizes, buy_orders] = \
                self.get_volume_size(bucket_string[i].time_start, bucket_string[i].time_end, levels)

            for j in range(0, levels):
                bucket_string[i].ask_volume_levels["level" + str(j)] = ask_sizes[j]
                bucket_string[i].bid_volume_levels["level" + str(j)] = bid_sizes[j]

            bucket_string[i].best_ask_price = ask_prices[0]  # change this to log price
            bucket_string[i].best_bid_price = bid_prices[0]
            bucket_string[i].ask_frequency = sell_orders
            bucket_string[i].bid_frequency = buy_orders
        """
        need to make this dynamic
          [ best log ask price,
            best log bid price,
            ask volume l1,
            ask volume l2,
            ask volume l3,
            bid volume l1,
            bid volume l2,
            bid volume l3,
            Sell,
            Buy ]
        """
        return bucket_string

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
