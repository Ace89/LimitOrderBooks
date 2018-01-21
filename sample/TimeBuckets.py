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

Work in nancoseconds as python only goes as far as milliseconds, when time is converted go
up to millisecond precision

"""
import numpy as np
import pandas as pd
from sample.Bucket import Bucket
from sample.Order import Order, OrderType, Direction, Visibility


class TimeBuckets:  # sequence of time buckets

    def __init__(self, data_frame, start_time, end_time, buckets):
        if type(data_frame) == pd.DataFrame:
            print('yee ha!')

        if start_time >= end_time:
            print("start time should be earlier than end time.")

        self.dataFrame = data_frame
        self.rows, self.cols = np.shape(data_frame)
        self.start_time = start_time
        self.end_time = end_time
        self.buckets = buckets

    @staticmethod
    def __all__():
        return ["count_if", "create_order_book_trees", "calculate_average_values_per_bucket",
                "create_order_book_tree_buckets", "create_order_book_average_buckets"]

    @staticmethod
    def __doc__():
        return "act as a data structure for message data"

    @staticmethod
    def count_if(matrix, col_num, value):
        
        count = 0
        
        for i in range(0, len(matrix)):
            if matrix[i, col_num] == value:
                count += 1
        
        return count

    def create_order_book_trees(self, time_start, time_end, levels=3):
        """
        :param time_start: this is local time_start  i.e. 34,200 , 34,500, 34,800
        :param time_end: this is local time_end i.e. 34,500 , 34,800, 35,100
        :param levels: this is the number of price levels
        :return: returns an order book tree object for the interval specified by time_start and time_end
        """

        data_matrix = self.dataFrame.as_matrix()
        size_data = len(data_matrix)
        count = 0
        sell_price = []
        buy_price = []
        """
            This is necessary as time start increases from the first value in data_matrix
            If I do not do this then the while condition will not be satisfied hence I will get null
            values
        """
        while count < size_data and data_matrix[count, 0] < time_start:
            count += 1

        lower_bound_count = count

        # collect prices for new sell/buy limit orders
        while count < size_data and time_start <= data_matrix[count, 0] < time_end:
            if data_matrix[count, 1] == 1 and data_matrix[count, 5] == -1: # only consider new limit orders
                if data_matrix[count, 4] not in sell_price:# so we only collect unique values
                    sell_price.append(data_matrix[count, 4])
            if data_matrix[count, 1] == 1 and data_matrix[count, 5] == 1:
                if data_matrix[count, 4] not in buy_price:
                    buy_price.append(data_matrix[count, 4])
            count += 1

        # sort buy/sell prices and select top levels and get volumes for each level

        sell_price.sort(reverse=False)# lowest to highest
        buy_price.sort(reverse=True)# highest to lowest

        buy_levels = {}
        sell_levels = {}

        # for each price get the volumes array
        if len(buy_price) != 0:
            for i in range(0, levels):
                price = buy_price[i]
                volumes = []
                count = lower_bound_count
                while count < size_data and time_start <= data_matrix[count, 0] < time_end:
                    if data_matrix[count, 1] == 1 and data_matrix[count, 5] == 1 and data_matrix[count, 4] == price:
                        volumes.append(data_matrix[count, 3])
                    count += 1
                buy_levels[price] = volumes

        if len(sell_price) != 0:
            for i in range(0, levels):
                price = sell_price[i]
                volumes = []
                count = lower_bound_count
                while count < size_data and time_start <= data_matrix[count, 0] < time_end:
                    if data_matrix[count, 1] == 1 and data_matrix[count, 5] == -1 and data_matrix[count, 4] == price:
                        volumes.append(data_matrix[count, 3])
                    count += 1
                sell_levels[price] = volumes

        order_book_tree = OrderBookTree(time_start, time_end, buy_levels, sell_levels)

        return order_book_tree

    def calculate_average_values_per_bucket(self, time_start, time_end, order_type):
        """
        :param time_start: this is local time_start
        :param time_end: this is local time_end
        :param order_type: -1 for sell order and 1 for buy orders
        :return: average price, average size and cumulative volume for time interval
        """

        data_matrix = self.dataFrame.as_matrix()

        count = 0
        size_data = len(data_matrix)
        price = []
        size = []

        while count < size_data and data_matrix[count, 0] < time_start:
            count += 1

        while count < size_data and time_start <= data_matrix[count, 0] < time_end:
            if data_matrix[count, 1] == 4 or data_matrix[count, 1] == 5:  # only consider execution orders
                if data_matrix[count, 5] == order_type:
                    price.append(data_matrix[count, 4])
                    size.append(data_matrix[count, 3])
            count += 1

        if len(price) != 0:
            avg_price = np.average(price)
            avg_size = np.average(size)
            cum_volume = np.sum(size)
        else:
            avg_price = 0
            avg_size = 0
            cum_volume = 0

        return [avg_price, avg_size, cum_volume]

    def get_limit_order_tree_buckets(self, time_start, time_end, nbins):
        """
        :param time_start: start time for interval
        :param time_end: end time for interval
        :param nbins: bins for histograms
        :return: bins and freq for sell and buy prices
        """
        data_matrix = self.dataFrame.as_matrix()
        size_data = len(data_matrix)
        count = 0
        sell_price = []
        buy_price = []

        while count < size_data and data_matrix[count, 0] < time_start:
            count += 1

        # collect prices for new sell/buy limit orders
        while count < size_data and time_start <= data_matrix[count, 0] < time_end:
            if data_matrix[count, 1] == 1 and data_matrix[count, 5] == -1: # only consider new limit orders
                sell_price.append(data_matrix[count, 4])
            if data_matrix[count, 1] == 1 and data_matrix[count, 5] == 1:
                buy_price.append(data_matrix[count, 4])
            count += 1

        sell_dict = self.create_bins_freq(sell_price, nbins)
        buy_dict = self.create_bins_freq(buy_price, nbins)

        return [buy_dict, sell_dict]

    @staticmethod
    def create_bins_freq(price, nbins):
        min_price = np.min(price)
        max_price = np.max(price)
        price_bins = list()
        price_bins.append(min_price)

        price_dict = {}

        for i in range(1, nbins):
            price_bins.append(price_bins[i - 1] + (max_price - min_price) / (nbins - 1))

        cumulative = 0

        for i in range(0, nbins):
            count = 0
            for j in range(0, len(price)):
                if price[j] <= price_bins[i]:
                    count += 1
            if i == 0:
                price_dict[price_bins[i]] = count
            else:
                cumulative = 0

                for key in price_dict:
                    cumulative += price_dict[key]

                price_dict[price_bins[i]] = count - cumulative

        return price_dict

    def create_order_book_tree_buckets(self, num_of_levels=3):

        intervals = (self.end_time - self.start_time) / self.buckets
        bucket_string = []

        for i in range(1, self.buckets+1):
            start_time = self.start_time + (i-1)*intervals
            end_time = self.start_time + i*intervals
            bucket_string.append(self.create_order_book_trees(start_time, end_time, num_of_levels))

        return bucket_string

    def create_order_book_average_buckets(self):
        # shift 'intervals' into the constructor
        intervals = (self.end_time - self.start_time) / self.buckets
        sell_bucket_string = []
        buy_bucket_string = []

        for i in range(1, self.buckets+1):
            start_time = self.start_time + (i-1)*intervals
            end_time = self.start_time + i*intervals
            sell_bucket_string.append(self.calculate_average_values_per_bucket(start_time, end_time, -1))# sell buckets
            buy_bucket_string.append(self.calculate_average_values_per_bucket(start_time, end_time, 1))# buy buckets

        return [buy_bucket_string, sell_bucket_string]

    def create_limit_order_tree_buckets(self, nbins = 50):
        intervals = (self.end_time - self.start_time) / self.buckets
        sell_bucket_dict = []
        buy_bucket_dict = []

        for i in range(1, self.buckets+1):
            start_time = self.start_time + (i-1)*intervals
            end_time = self.start_time + i*intervals
            [buy_buckets, sell_buckets] = self.get_limit_order_tree_buckets(start_time, end_time, nbins)
            buy_bucket_dict.append(buy_buckets)
            sell_bucket_dict.append(sell_buckets)

        return [buy_bucket_dict, sell_bucket_dict]


class OrderBookTree:

    @staticmethod
    def __doc__():
        return "contains number of levels of interest in the order book, dictionaries for prices " \
               "and list of volumes for that price"

    def __init__(self, start_time, end_time, buy_levels, sell_levels, levels=3):
        self.start_time = start_time
        self.end_time = end_time
        self.levels = levels
        self.buy_levels = buy_levels
        self.sell_levels = sell_levels
