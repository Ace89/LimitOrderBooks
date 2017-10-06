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


class TimeBuckets:

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
