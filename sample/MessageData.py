"""
    Aim:
        Take data from csv file as matrix and split into lists and variables

    Data Matrix Columns:
        Time, Type, OrderId, Size, Price, Direction

    First thing would be to read all messages into a dictonary/time buckets

    Hidden orders will not have a tradeid, it will be 0


    Two very distinct tasks:
    -> Message Data to read in data from CSV file and put into time Bucket
    -> Time Bucket to be used to perform any analysis on the data
    -> Types of analysis includes: fitting vol i.e. EWMA
    -> Forecasting volume
    -> Forecasting short term prices

    Take out anything related to summary and display and move to another class

"""

import pandas as pd
import numpy as np
from sample.OrderFactory import OrderFactory
from sample.Order import ExecutionType, Visibility, Direction, OrderType
from sample.TimeBuckets import TimeBuckets
from sample.PriceLevel import PriceLevel

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data', 'read', 'short_summary', 'summary',
           'display', 'supply_demand', 'plot', 'get_buy_sell_prices','price_volatility']


class MessageData:

    seconds_in_hour = 60.0*60.0  # static variable
    order_factory = OrderFactory()

    @staticmethod
    def __doc__():
        return "Aim of this class is to read in data given a csv file"

    def __init__(self, file_location):
        self.data_frame = pd.read_csv(file_location)
        self.data_matrix = self.data_frame.as_matrix()
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

        return None

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

    def convert_to_timeseries(self):
        """
        Convert time bucket into a time series  i.e.
        take all the best bid prices from string of buckets and put them into a DataSeries etc
        """
        start = self.start_time
        return None

    def read(self, start_time, end_time, num_of_buckets):
        # read values from data_matrix up to index
        time_buckets = TimeBuckets(self.data_frame, start_time, end_time, num_of_buckets)
        # self.current_matrix = np.matrix(self.data_matrix[0:index, :])
        return time_buckets