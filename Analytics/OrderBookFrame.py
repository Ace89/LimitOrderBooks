
import pandas as pd
import numpy as np
from Time.TimeStructure import TimeStructure
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Enums.DataType import DataType
import datetime

"""
data frame has methods like:
    data
    columns
    index
    dtype
    copy
"""

"""
Read in csv and create a raw order book frame

methods:
    group into time buckets
    kurtosis
    volatility - be able to provide a method
    fit distribution - specify teh distribution to be fitted
"""
"""
Time

OrderType :-
    1) Submission of a new order
    2) Cancellation or deletion of an order
    3) Deletion of an order
    4) Execution of a visible order
    5) Execution of a hidden order
    7) Trading halt

OrderId

Size :- Number of shares

Price :- Dollar price time 10,000

Direction :- -1 sell, 1 but order

"""


class OrderBookFrame():

    def __init__(self, data):
        """
        :param data: data frame containing raw data
        """
        self.df = data
        self.df.columns = ['Time', 'OrderType', 'OrderId', 'Size', 'Price', 'Direction']
        self.start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
        self.end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
        self.date = datetime.datetime(year=2012, month=6, day=21)
        self.BuyTimeStructure = TimeStructure(self.start_date, self.end_date)
        self.BuyTimeStructure.create_time_structure(intervals=300)
        self.ticker = 'AMZN'
        self.__create_time_bucket_structure(self.BuyTimeStructure, OrderType.VisibleExecution, OrderDirection.Buy)
        self.SellTimeStructure = TimeStructure(self.start_date, self.end_date)
        self.SellTimeStructure.create_time_structure(intervals=300)
        self.__create_time_bucket_structure(self.SellTimeStructure, OrderType.VisibleExecution, OrderDirection.Sell)
        self.__initialize()
        # Time should be in the index

    @staticmethod
    def __convert_datetime_to_seconds(date_time):
        """
        if type(datetime) != datetime:
            raise Exception('date time must be of type datetime')
        """
        result = date_time.hour * 3600 + date_time.minute * 60 + date_time.second + date_time.microsecond * 1000000
        return result

    @staticmethod
    def __filter_data_matrix(data, order_type_filter, order_direction_filter):
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

    def __create_time_bucket_structure(self, timeStructure, order_type, order_direction):
        """
        :param timeStructure: TimeStructure object
        :param order_type: limit orders or executed orders
        :param order_direction: buy prices or sell prices
        :return: populated time structure with average price and average volume
        """
        # put the data into the time series buckets
        # for now just the average prices
        # split for submission prices and execution prices

        data = self.df.as_matrix()
        order_type_vals = (data[:, 1] == order_type.value)
        order_direction_vals = (data[:, 5] == order_direction.value)

        filtered_data = OrderBookFrame.__filter_data_matrix(data, order_type_vals, order_direction_vals)

        for structure in timeStructure.time_structure:
            temp_start_time = OrderBookFrame.__convert_datetime_to_seconds(structure.start_time)
            temp_end_time = OrderBookFrame.__convert_datetime_to_seconds(structure.end_time)
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

    def __initialize(self):
        # index- order type - average buy price - buy volume - average sell price - sell volume
        buy_price_series = self.BuyTimeStructure.create_time_series()
        buy_volume = self.BuyTimeStructure.create_volume_series()
        sell_price_series = self.SellTimeStructure.create_time_series()
        sell_volume = self.SellTimeStructure.create_volume_series()
        index = self.BuyTimeStructure.create_time_index()
        # create a new data frame with the
        self.data_frame = pd.DataFrame(buy_price_series, columns=['BuyPrice'], index=index)
        self.data_frame['BuyVolume'] = pd.Series(buy_volume, index=index)
        self.data_frame['SellPrice'] = pd.Series(sell_price_series, index=index)
        self.data_frame['SellVolume'] = pd.Series(sell_volume, index=index)

    def summary_statistics(self, column_name=None):
        """
        :param column_name:
        :return:
        """
        output = {}

        attributes = [np.average, np.median]

        if column_name is None:
            for column in self.data_frame.columns:
                cont=list()
                for atts in attributes:
                    cont.append(atts(self.data_frame[column].tolist()))
                output[column] = cont
        else:
            cont = [atts(self.data_frame[column_name].tolist()) for atts in attributes]
            output[column_name] = cont

        return cont

    # not sure this method is needed
    def add_column(self, column_name, data):

        if column_name in self.data_frame.columns:
            raise ValueError('Column name already exists')

        if isinstance(data, pd.Series):
            self.data_frame[column_name] = data
        else:
            series = pd.Series(data)
            self.data_frame[column_name] = series

    def add_time_buckets(self, start_time, end_time, intervals):
        # rename this to add index, index will be time buckets
        time_structure = TimeStructure(start_time, end_time)
        time_structure.create_time_structure(intervals)

        self.data_frame.index = time_structure.time_structure

    def volatility(self, column_name=None, methodtype='standard_deviation'):

        if column_name is None:
            output = [np.std(self.data_frame[column].tolist()) for column in self.data_frame.columns]
        else:
            output = [np.std(self.data_frame[column_name].tolist())]

        return output

    def kurtosis(self, column_name=None):
        if column_name is None:
            output = [np.kurt(self.data_frame[column].tolist()) for column in self.data_frame.columns]
        else:
            output = [np.kurt(self.data_frame[column_name].tolist())]

        return output

    def remove_outliers(self, column_name=None):
        """
        :param column_name: name of column to remove outliers from
        :return: dataframe with the outliers removed
        """

        if column_name is None or column_name not in self.data_frame.columns:
            raise ValueError('Please provide a valid column name')

        time_series = self.data_frame[column_name].tolist()

        mu = np.average(time_series)
        std = np.std(time_series)
        lb = mu - 1.5*std
        ub = mu + 1.5*std

        remove_index = list()

        for i in range(0, len(time_series)):
            if time_series[i] < lb:
                remove_index.append(i)
                continue
            if time_series[i] > ub:
                remove_index.append(i)
                continue

        self.data_frame.drop(self.data_frame.index[remove_index])

    def order_book_imbalance(self):
        """
        :return: a series of order book imbalance
        """

        imbalance = [self.data_frame['BuyOrders'][idx] / self.data_frame['SellOrders'][idx] for idx in self.data_frame.index]

        self.data_frame['Imbalance'] = pd.Series(imbalance)

    def plot(self):
        """
        :return: output a diagram
        """
        pass

 
if __name__ == '__main__':
    import datetime
    from Data.TimeSeriesRepository import TimeSeriesRepository
    import matplotlib.pyplot as plt
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    ticker ='AMZN'
    date = datetime.datetime(year=2012, month=6, day=21)
    classifier = DataType.message
    timestamp = 5

    time_series_repository = TimeSeriesRepository(file_path)
    data = time_series_repository.get_data(ticker, date, classifier, timestamp)
    order_book_frame = OrderBookFrame(data)
    vol = order_book_frame.volatility()

    for val in vol:
        print(val)
