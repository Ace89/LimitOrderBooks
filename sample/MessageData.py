"""
    Aim:
        Take data from csv file as matrix and split into lists and variables

    Data Matrix Columns:
        Time, Type, OrderId, Size, Price, Direction

    First thing would be to read all messages into a dictonary

    Hidden orders will not have a tradeid, it will be 0

"""

import pandas as pd
import numpy as np
from sample.OrderFactory import OrderFactory
from sample.Order import ExecutionType, Visibility, Direction, OrderType
from sample.PriceLevel import PriceLevel
import matplotlib.pyplot as plt

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['sort_price_levels', 'unpack_orders', 'unpack_data', 'read', 'short_summary', 'summary',
           '_sort_price_levels', 'display', 'supply_demand', 'plot', 'get_buy_sell_prices',
           'price_volatility']


class MessageData:

    seconds_in_hour = 60.0*60.0  # static variable
    order_factory = OrderFactory()

    def __init__(self, file):
        self.data_matrix = pd.read_csv(file).as_matrix()
        # throw an error message if data_matrix is not of type matrix
        self.sell_orders = 0
        self.buy_orders = 0
        self.bids = []
        self.offers = []
        self.time_stamps = []
        self.exec_prices = []
        self.volumes = self.data_matrix[:, 3]
        self.new_limit_order = 0
        self.order_cancel = 0
        self.order_delete = 0
        self.exec_visible_order = 0
        self.exec_hidden_Order = 0
        self.trading_halt = 0
        self.orders = {}

    def sort_price_levels(self, price_levels):
        # get an infinite loop here
        changes = 1
        while changes > 0:
            changes = 0
            for i in range(1, len(price_levels)):
                if price_levels[i-1] > price_levels[i]:
                    changes += 1
                    a = price_levels[i]
                    b = price_levels[i-1]
                    price_levels[i-1] = a
                    price_levels[i] = b

        return None

    def unpack_orders(self):  # similar to read

        for row in self.data_matrix:
            order_time = row[0]
            order_type = row[1]
            order_id = row[2]
            order_volume = row[3]
            order_price = row[4]
            order_direction = row[5]

            # if order already exists then either it has been filled or cancelled partially or fully

            if order_id in self.orders:
                temp_order = self.orders[order_id]
                if order_type == 2 or order_type == 3:
                    temp_order.cancel_order(order_time, order_volume)
                else:
                    temp_order.execute_order(order_time, order_volume)
                self.orders[order_id] = temp_order
            else:
                if order_id == 0:  # hidden order
                    order = MessageData.order_factory.create_order(order_time, order_direction, order_price,
                                                                   order_volume, Visibility.Hidden, order_type)
                    order_id = order.__hash__()
                else:  # visible order
                    order = MessageData.order_factory.create_order(order_time, order_direction, order_price,
                                                                   order_volume, Visibility.Visible, order_type)
                self.orders[order_id] = order

    def unpack_data(self):  # similar to summary
        #  Collect time stamps, bid and offer values as well as number of buy and sell orders
        for i in range(0, len(self.data_matrix[:, 4])):
            self.time_stamps.append(self.data_matrix[i, 0] / self.seconds_in_hour)
            if self.data_matrix[i, 5] == -1:
                self.sell_orders += 1
                self.bids.append(self.data_matrix[i, 4] / 10000)
            else:
                self.buy_orders += 1
                self.offers.append(self.data_matrix[i, 4] / 10000)
        #  Collect type of order
        for i in range(0, len(self.data_matrix[:, 1])):
            if self.data_matrix[i, 1] == 1:
                self.new_limit_order += 1
            elif self.data_matrix[i, 1] == 2:
                self.order_cancel += 1
            elif self.data_matrix[i, 1] == 3:
                self.order_delete += 1
            elif self.data_matrix[i, 1] == 4:
                self.exec_visible_order += 1
                self.exec_prices.append(self.data_matrix[i, 4] / 10000)
            elif self.data_matrix[i, 1] == 5:
                self.exec_hidden_Order += 1
                self.exec_prices.append(self.data_matrix[i, 4] / 10000)
            else:
                self.trading_halt += 1

        return [self.sell_orders, self.buy_orders, self.bids, self.offers, self.time_stamps, self.exec_prices]

    def read(self, index):
        # read values from data_matrix up to index
        self.current_matrix = np.matrix(self.data_matrix[0:index, :])
        None

    def short_summary(self):
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows-1,0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor)*60.0
        bids = 0
        offers = 0

        for i in range(0, rows):
            if self.current_matrix[i,1] == 1:
                if self.current_matrix[i, 5] == 1:
                    bids += 1
                else:
                    offers += 1

        print('\nCurrent order book time: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))
        print('Message Index: {0:5d}'.format(rows))
        print('Bid Orders: {0:5d}'.format(bids))
        print('Ask Orders: {0:5d}'.format(offers))
        print('Total Orders: {0:5d}'.format(bids+offers))
        None

    def summary(self):
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows-1, 0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor)*60.0
        bids = 0
        offers = 0

        for i in range(0, rows):
            if self.current_matrix[i, 1] == 1:
                if self.current_matrix[i, 5] == 1:
                    bids += 1
                else:
                    offers += 1

        print('\nCurrent order book time: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))
        print('Message Index: {0:5d}'.format(rows))
        print('Bid Orders: {0:5d}'.format(bids))
        print('Ask Orders: {0:5d}'.format(offers))
        print('Total Orders: {0:5d}'.format(bids+offers))
        None

    def _sort_price_levels(self): # private method
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows - 1, 0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor) * 60.0

        bid_price_range = []
        offer_price_range = []
        for i in range(0, rows):
            if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 5] == 1:
                bid_price_range.append(self.current_matrix[i, 4])
            elif self.current_matrix[i, 1] == 1 and self.current_matrix[i, 5] == -1:
                offer_price_range.append(self.current_matrix[i, 4])
        bid_price_range = np.array(bid_price_range)
        bid_price_range = np.unique(bid_price_range)
        offer_price_range = np.array(offer_price_range)
        offer_price_range = np.unique(offer_price_range)

        bid_levels = []  # contains price level objects
        offer_levels = []  # contains price level objects
        # differentiate between bid and ask price levels
        for val in bid_price_range:
            # create a price level object
            bid_price_level = PriceLevel(val)
            for i in range(0, rows):
                if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 4] == val and self.current_matrix[i, 5] == 1:
                    bid_price_level.add_volume(self.current_matrix[i, 3])
            bid_levels.append(bid_price_level)

        for val in offer_price_range:
            # create a price level object
            offer_price_level = PriceLevel(val)
            for i in range(0, rows):
                if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 4] == val and self.current_matrix[i, 5] == -1:
                    offer_price_level.add_volume(self.current_matrix[i, 3])
            offer_levels.append(offer_price_level)

        print('Current time is: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))

        self.sort_price_levels(bid_levels)
        self.sort_price_levels(offer_levels)
        return [bid_levels, offer_levels]

    def display(self):

        [bid_levels, offer_levels] = self._sort_price_levels()

        for i in range(0, 5):
            print('{0} --- {1}'.format(bid_levels[i].get_price(), bid_levels[i].get_volumes()[0]))

        print('---------------------------------------------------')

        for i in range(0, 5):
            print('{0} --- {1}'.format(offer_levels[i].get_price(), offer_levels[i].get_volumes()[0]))

        None

    def supply_demand(self):
        # normalize price levels using the absolute difference between best ask and mid price
        # normalize volume levels using sum of sizes across all plotted price levels on each side
        # first calculate mid price, then best ask price

        [bid_levels, offer_levels] = self._sort_price_levels()

        mid_price = (offer_levels[0].get_price() + bid_levels[-1].get_price()) * 0.50

        ask_price_normalize = np.abs(offer_levels[-1].get_price() - mid_price)
        ask_price = []
        ask_volume_normalize = 0.0
        ask_volume = []
        size = len(offer_levels)

        for i in range(0, size):
            ask_price.append(offer_levels[i].get_price() / ask_price_normalize)
            ask_volume_normalize += np.sum(offer_levels[i].get_volumes())

        for i in range(0, size):
            ask_volume.append(np.sum(offer_levels[i].get_volumes())/ask_volume_normalize)

        self.sort_price_levels(ask_volume)
        self.sort_price_levels(ask_price)

        plt.plot(ask_volume, ask_price)
        plt.show()
        # last value in bid_levels is the best bid price
        # first value in offer levels is the best ask price
        # diff of two is the mid

        return None

    def plot(self):
        pass

    def get_buy_sell_prices(self):
        rows, cols = np.shape(self.current_matrix)
        buy_prices = []
        sell_prices = []

        for i in range(0, rows):
            if self.current_matrix[i, 1] == 4 or self.current_matrix[i, 1] == 5:
                if self.current_matrix[i, 5] == 1:
                    buy_prices.append(self.current_matrix[i, 4])
                else:
                    sell_prices.append(self.current_matrix[i, 4])

        return buy_prices, sell_prices

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

        for i in range(1,len(sell_prices)):
            sell_rets.append(np.log(sell_prices[i]/sell_prices[i-1]))

        return np.std(buy_rets), np.std(sell_rets)