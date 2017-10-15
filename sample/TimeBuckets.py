#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:39:06 2017

@author: ace89

Will need to filter by buy limit orders and sell limit orders
Another consideration is type of order: new limit order, cancellation, deletion,
execution of visible limit order, execution of hidden order, trading halt 
indicator is negligible

When you read a CSV, we get an object called a DataFrame, this is made up of rows and 
columns. You get columns out of a DataFrame same way you get values out of a dictionary.

If you take a column out, you get a Series

Issue is that, there are duplicate values in the time column, so if time is used as an 
index then some of the values stored against that key are floats and some are series

DataFrame is taken from pandas

"""
import numpy as np
from sample.Order import Order, OrderType, Direction, Visibility


class Bucket:

    def __init__(self, time_start, time_end, ask_price, bid_price,ask_freq,bid_freq):
        self.time_start = time_start
        self.time_end = time_end
        self.best_ask_price = ask_price
        self.best_bid_price = bid_price
        self.ask_volume_levels = {}  # keys to these dictionaries will be "level 1", "level 2" ... etc
        self.bid_volume_levels = {}
        self.ask_frequency = ask_freq
        self.buy_frequency = bid_freq

    def init_volume_levels(self, levels):

        for i in (0,levels):
            key = "level" + str(i)
            self.ask_volume_levels[key] = 0
            self.bid_volume_levels[key] = 0


class TimeBuckets:  # sequence of time buckets

    def __init__(self, data_frame):
        self.dataFrame = data_frame
        self.rows, self.cols = np.shape(data_frame)

    def append_column_names(self, column_names):
        if len(column_names) != self.cols:
            raise ValueError('length of column names should equal columns in data frame')

        self.dataFrame.columns = column_names
        return None

    @staticmethod
    def count_if(matrix, col_num, value):
        
        count = 0
        
        for i in range(0, len(matrix)):
            if matrix[i, col_num] == value:
                count += 1
        
        return count

    def create_time_buckets(self, time_start, time_end, num_buckets, order_type):
        """
        For each order type, return 2 dataframes one for sells and one for buys
        Do not average volume data, return accumulation in time bucket
        """
        intervals = (time_end-time_start)/num_buckets
        
        buckets = list([])
        buckets.append(0)  # first value will be time_start, so we will have num_buckets + 1 values
        for i in range(1, num_buckets+1):
            buckets.append(time_start + i*intervals)
            
        data_matrix = self.dataFrame.as_matrix()

        count = 0
        size_data = len(data_matrix)

        avg_price = np.zeros(num_buckets)
        avg_size = np.zeros(num_buckets)
        cum_volume = np.zeros(num_buckets)  # cumulative volume

        for i in range(1, num_buckets+1):
            price = []
            size = []
            # count < len(data_matrix) and data_matrix[count,0] < buckets[i] and data_matrix[count,0] >= buckets[i-1]
            while count < size_data and buckets[i-1] <= data_matrix[count, 0] < buckets[i]:
                if data_matrix[count, 1] == 4 or data_matrix[count, 1] == 5:  # only consider execution orders
                    if data_matrix[count, 5] == order_type:
                        price.append(data_matrix[count, 4])
                        size.append(data_matrix[count, 3])
                count += 1
            if len(price) != 0:
                avg_price[i-1] = np.average(price)
                avg_size[i-1] = np.average(size)
                cum_volume[i-1] = np.sum(size)
            else:            
                avg_price[i-1] = 0
                avg_size[i-1] = 0
                cum_volume[i-1] = 0

        return [buckets, avg_price, avg_size, cum_volume]

    def time_bucket(self, time_start, time_end, num_buckets, levels):

        bucket_string = []
        intervals = (time_end - time_start) / num_buckets
        bucket_string.append(0)

        for i in range(1, num_buckets+1):
            bucket = Bucket(time_start + (i-1)*intervals, time_start + i*intervals, 0, 0, 0, 0)
            bucket_string.append(bucket)

        for i in range(1, num_buckets+1):
            # count is just to make sure I do not exceed the matrix dimensions
            [ask_prices, ask_sizes, sell_orders, bid_prices,bid_sizes, buy_orders] = self._get_volume_size(bucket_string[i].time_start, bucket_string[i].time_end, levels)

            for j in range(0, levels):
                bucket_string[i].ask_volume_levels["level" + str(j)] = ask_sizes[j]
                bucket_string[i].bid_volume_levels["level" + str(j)] = bid_sizes[j]

            bucket_string[i].best_ask_price = ask_prices[0]  # change this to log price
            bucket_string[i].best_bid_price = bid_prices[0]
            bucket_string[i].ask_frequency = sell_orders
            bucket_string[i].bid_frequency = buy_orders
        """
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

    def _get_volume_size(self, time_start, time_end, levels):
        # check for unique orders, filter
        # zero is the best level
        orders = []
        data_matrix = self.dataFrame.as_matrix()
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
                order = Order(data_matrix[count,0],direction,data_matrix[count,4],data_matrix[count,3],visibility,OrderType.Submission)
                orders.append(order)
            count += 1

        # get submisison order information
        if len(orders) == 0:
            print("no orders")

        [ask_prices, ask_sizes, sell_orders] = self._get_level_stats(orders, -1, levels)
        [bid_prices, bid_sizes, buy_orders] = self._get_level_stats(orders, 1, levels)
        # go through the list of orders and for each price see how many copies of the same price

        return [ask_prices, ask_sizes, sell_orders, bid_prices, bid_sizes, buy_orders]

    @staticmethod
    def _get_level_stats(orders, bid_ask, levels):
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
