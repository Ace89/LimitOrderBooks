
from Analytics.LimitOrderBook.DataReader import DataReader
from Analytics.LimitOrderBook.DataReaderResult import DataReaderResult


class OrderBookDataReader(DataReader):

    def __init__(self, message_data_file):
        self.levels = None
        self.message_data_file = message_data_file

    def read_data(self, message_file):
        """
        :param message_file: file containing data
        :return: data frame containing prices and sizes
        """
        import pandas as pd
        msg_data = pd.read_csv(self.message_data_file)
        data = pd.read_csv(message_file)
        data.index = msg_data['Time']
        self.levels = len(data.columns) / 4

        return data


if __name__ == '__main__':
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'
    msg_file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
    data_reader = OrderBookDataReader(file_path+msg_file_name)
    data = data_reader.read_data(file_path+file_name)
    print('loaded successfully')
