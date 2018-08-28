
from Enums.TimeSeriesTypes import TimeSeriesTypes

import numpy as np
import pandas as pd


class TimeSeriesFactory:

    def __init__(self, limit_order_books):
        self.books = limit_order_books
        self.err_msg = 'series type not recognised'

    def create_time_series(self, time_series_types, start_time=34200, time_interval=5):
        """
        :param time_series_types: time series type
        :param start_time: start time
        :param time_interval: time interval
        :return: time series as list
        """
        if time_series_types == TimeSeriesTypes.price:
            bid_output = list()
            ask_output = list()
            index = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    bid_output.append(book[0][-1].price)
                    ask_output.append(book[1][0].price)
                    index.append(start_time)
                    start_time += time_interval
            return pd.Series(bid_output, index=index), pd.Series(ask_output, index=index)
        elif time_series_types == TimeSeriesTypes.size:
            bid_output = list()
            ask_output = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    bid_output.append(book[0][-1].size)
                    ask_output.append(book[1][0].size)
                    start_time += time_interval
            return bid_output, ask_output
        elif time_series_types == TimeSeriesTypes.full_size:
            bid_output = list()
            ask_output = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    bid_orders = [book[0][i].size for i in range(0, len(book[0]))]
                    ask_orders = [book[1][i].size for i in range(0, len(book[1]))]
                    bid_output.append(np.sum(bid_orders))
                    ask_output.append(np.sum(ask_orders))
                    start_time += time_interval
            return bid_output, ask_output
        elif time_series_types == TimeSeriesTypes.mid_price:
            bid_price, ask_price = self.create_time_series(start_time, time_interval, series_type=TimeSeriesTypes.price)
            mid_price = list()
            for i in range(0, len(bid_price)):
                mid_price.append(0.5 * (bid_price[i] + ask_price[i]))
            return mid_price
        elif time_series_types == TimeSeriesTypes.imbalance:
            imbalance_output = list()
            index = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    imbalance_output.append(book[1][0].price - book[0][-1].price)
                    index.append(start_time)
                    start_time += time_interval
            return pd.Series(imbalance_output, index=index)
        else:
            raise NotImplementedError(self.err_msg)
