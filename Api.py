
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook


file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
order_file = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'


def reconstruct_order_book(file, data_type):
    """
    :param file: Data file
    :param data_type: Message data or Order data
    :return: A collection of books
    """
    limit_order_book = LimitOrderBook()

    if data_type == 'message':
        data_reader = MessageDataReader()
    elif data_type == 'order':
        data_reader = OrderBookDataReader()
    else:
        raise NotImplementedError('Data type not recognised')

    data_reader.read_data(file)
    lob_updater = LimitOrderBookUpdater(data_reader.messages)
    lob_updater.update_order_book(limit_order_book)

    return lob_updater.books

