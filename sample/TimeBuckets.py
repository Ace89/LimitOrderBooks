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
from datetime import date, timedelta


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
        return ["append_column_names", "count_if", "create_time_buckets", "time_bucket"]

    @staticmethod
    def __doc__():
        return "act as a data structure for message data"

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

    def create_time_buckets(self, order_type):
        """
        For each order type, return 2 data frames one for sells and one for buys
        Do not average volume data, return accumulation in time bucket
        """
        intervals = (self.end_time-self.start_time)/self.buckets
        
        buckets = list([])
        buckets.append(0)  # first value will be time_start, so we will have num_buckets + 1 values
        for i in range(1, self.buckets):
            buckets.append(self.start_time + i*intervals)
            
        data_matrix = self.dataFrame.as_matrix()

        count = 0
        size_data = len(data_matrix)

        avg_price = np.zeros(self.buckets)
        avg_size = np.zeros(self.buckets)
        cum_volume = np.zeros(self.buckets)  # cumulative volume

        for i in range(1, self.buckets+1):
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


