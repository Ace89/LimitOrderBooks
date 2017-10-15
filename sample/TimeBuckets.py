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

    def __init__(self):
        self.time_start
        self.time_end
        self.best_ask_price
        self.best_bid_price
        self.ask_volume_levels = {}  # keys to these dictionaries will be "level 1", "level 2" ... etc
        self.bid_volume_levels = {}
        self.ask_frequency
        self.buy_frequency

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

        data_matrix = self.dataFrame.as_matrix()
        bucket_string = []
        intervals = (time_end - time_start) / num_buckets
        bucket_string.append(0)

        size_data = len(data_matrix)
        count = 0

        for i in range(1, num_buckets+1):
            bucket = Bucket()
            bucket.time_start = time_start + (i-1)*intervals
            bucket.time_end = time_start + i*intervals
            bucket_string.append(bucket)

        for i in range(1, num_buckets+1):
            ask_price = []
            bid_price = []
            size = []
            while count < size_data and bucket_string[i].time_start <= data_matrix[count, 0] \
                    < bucket_string[i].time_end:
                if data_matrix[count, 1] == 4 or data_matrix[count, 1] == 5:
                    if data_matrix[count, 5] == -1:
                        ask_price.append(data_matrix[count, 4])
                    else:
                        bid_price.append(data_matrix[count, 4])

                bucket_string[i].best_ask_price = np.max(ask_price)
                bucket_string[i].best_bid_price = np.max(bid_price)
                for j in range(0, levels):
                    bucket_string[i].ask_volume_levels["level" + str(j)] = self._get_volume_size()
                    bucket_string[i].bid_volume_levels["level" + str(j)] = self._get_volume_size()

                bucket_string[i].ask_frequency = 5  # call a method here
                bucket_string[i].bid_frequency = 5
                count += 1
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

    def _get_volume_size(self, time_start, time_end, bid_ask_indicator, bid_level):
        # -1 for ask
        # 1 for bid
        # check for unique orders, filter
        # zero is the best level
        orders = []
        data_matrix = self.dataFrame.as_matrix()
        orderType = OrderType(1)
        visibility = Visibility(1)
        count = 0
        while time_start < data_matrix[count, 0] <= time_end:
            if data_matrix[count, 1] == 1:   # only interested in new submission orders
                direction = Direction(data_matrix[count, 5])
                order = Order(data_matrix[count,0],direction,data_matrix[count,4],data_matrix[count,3],visibility)
                orders.append(order)
            count += 1

        # go through the list of orders and for each price see how many copies of the same price

        return None

    @staticmethod
    def _get_level_stats(self, orders, bid_ask, levels):

        for i in range(0, len(orders)):

            if orders[i].direction == Direction.Bid:
                print()

        return None