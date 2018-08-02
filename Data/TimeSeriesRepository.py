
import numpy as np
import pandas as pd
import datetime
from Time.TimeStructure import TimeStructure
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Enums.DataType import DataType


class TimeSeriesRepository:

    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def _convert_datetime_to_seconds(date_time):
        """
        if type(datetime) != datetime:
            raise Exception('date time must be of type datetime')
        """
        result = date_time.hour*3600 + date_time.minute*60 + date_time.second + date_time.microsecond*1000000
        return result

    @staticmethod
    def _create_file_name(ticker, date, classifier, time_stamp):

        if date.month < 10:
            _date = str(date.year) + '-0' + str(date.month) + '-' + str(date.day)
        else:
            _date = str(date.year) + '-' + str(date.month) + '-' + str(date.day)

        return ticker + "_" + str(_date) + "_34200000_57600000_" + classifier.name + "_" + str(time_stamp)+".csv"

    @staticmethod
    def _filter_data_matrix(data, order_type_filter, order_direction_filter):
        rows, cols = data.shape

        filtered_rows = 0

        for i in range(0, rows):
            if order_type_filter[i] == True and order_direction_filter[i] == True:
                filtered_rows += 1

        filtered_matrix = np.zeros((filtered_rows, cols))

        temp_rows = 0
        inner_rows = 0

        while temp_rows < rows or inner_rows < filtered_rows:
            if order_type_filter[temp_rows] == True and order_direction_filter[temp_rows] == True:
                filtered_matrix[inner_rows, :] = data[temp_rows, :]
                inner_rows += 1
            temp_rows += 1

        return filtered_matrix

    def get_data(self, ticker, date, classifier, time_stamp):
        """
        :param ticker: Stock ticker
        :param date: date of time series
        :param classifier: message data or order book data
        :param time_stamp: 5 minutes or 10 minutes
        :return: pandas data frame container
        """
        file_name = self._create_file_name(ticker, date, classifier, time_stamp)
        data = pd.read_csv(self.file_path + file_name)
        return data

    def create_time_bucket_structure(self, timeStructure, ticker, date, classifier, time_stamp, order_type, order_direction):
        """
        :param timeStructure: TimeStructure object
        :param ticker: Stock ticker
        :param date: date of data
        :param classifier: message data or object data, make this an enum
        :param time_stamp: 5 minute data or 10 minute data, make this an enum
        :param order_type: limit orders or executed orders
        :param order_direction: buy prices or sell prices
        :return: populated time structure with average price and average volume
        """
        # put the data into the time series buckets
        # for now just the average prices
        # split for submission prices and execution prices

        file_name = self._create_file_name(ticker, date, classifier, time_stamp)
        data = pd.read_csv(self.file_path + file_name).as_matrix()
        order_type_vals = (data[:, 1] == order_type.value)
        order_direction_vals = (data[:, 5] == order_direction.value)

        filtered_data = self._filter_data_matrix(data, order_type_vals, order_direction_vals)

        for structure in timeStructure.time_structure:
            temp_start_time = self._convert_datetime_to_seconds(structure.start_time)
            temp_end_time = self._convert_datetime_to_seconds(structure.end_time)
            temp_volumes = filtered_data[(temp_start_time <= filtered_data[:, 0]) & (filtered_data[:, 0] <= temp_end_time), 3]
            temp_prices = filtered_data[(temp_start_time <= filtered_data[:, 0]) & (filtered_data[:, 0] <= temp_end_time), 4]
            if order_direction == OrderDirection.Buy:
                structure.buy_orders = np.count_nonzero(temp_prices)
            elif order_direction == OrderDirection.Sell:
                structure.sell_orders = np.count_nonzero(temp_prices)

            if len(temp_volumes) != 0 or len(temp_prices) != 0:
                structure.set_volume(np.average(temp_volumes))
                structure.set_price(np.average(temp_prices))
            else:
                structure.set_volume(0.0)
                structure.set_price(0.0)

if __name__ == '__main__':
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    ticker = 'AMZN'
    file_name = 'AMZN_2012-06-21_34200000_57600000_message_5.csv'
    start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
    end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
    date = datetime.datetime(year=2012, month=6, day=21)
    timeSeriesRepository = TimeSeriesRepository(file_path)
    timeStructure = TimeStructure(start_date, end_date)
    timeStructure.create_time_structure(intervals=300)
    timeSeriesRepository.create_time_bucket_structure(timeStructure, ticker, date, DataType.message, 5,
                                                      OrderType.VisibleExecution, OrderDirection.Buy)
    print('Series created')
