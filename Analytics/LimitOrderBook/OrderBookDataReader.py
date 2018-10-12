
from Analytics.LimitOrderBook.IDataReader import IDataReader
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader


class OrderBookDataReader(IDataReader):

    def __init__(self, levels, message_file):
        self.messages = None
        self.message_file = message_file
        self.levels = levels
        self.headers = self.__generate_column_headers()

    def read_data(self, order_message_file):
        """
        :param order_message_file: file containing order book data
        :param message_file: file containing data
        :return: data frame containing prices and sizes
        """
        import pandas as pd

        msg_data_reader = MessageDataReader()
        msg_data = msg_data_reader.read_data_frame(self.message_file)

        data = pd.read_csv(order_message_file)
        data.columns = self.headers
        data['Time'] = msg_data['Time']
        self.messages = data
        return self.messages

    def __generate_column_headers(self):
        names = ['AskPrice', 'AskSize', 'BidPrice', 'BidSize']
        idx = list()
        cont = 1
        for i in range(1, self.levels*len(names)+1):
            idx.append(cont)
            if i % len(names) == 0:
                cont += 1

        headers = ['{0}{1}'.format(x, y) for x, y in zip(names*self.levels, idx)]
        return headers

if __name__ == '__main__':
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'
    msg_file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
    levels = 5
    data_reader = OrderBookDataReader(levels, file_path+msg_file_name)
    data = data_reader.read_data(file_path+file_name)
    print('loaded successfully')
