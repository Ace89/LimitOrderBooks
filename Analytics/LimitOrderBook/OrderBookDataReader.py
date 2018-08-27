
from Analytics.LimitOrderBook.DataReader import DataReader


class OrderBookDataReader(DataReader):

    def __init__(self):
        self.levels = None

    def read_data(self, message_file):
        """
        :param message_file: file containing data
        :return: data frame containing prices and sizes
        """
        import pandas as pd

        data = pd.read_csv(message_file)

        self.levels = len(data.columns) / 4

        return data


if __name__ == '__main__':
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'
    data_reader = OrderBookDataReader()
    data = data_reader.read_data(file_path+file_name)
    print('loaded successfully')
