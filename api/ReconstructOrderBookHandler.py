
import abc
from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader


class Handler(metaclass=abc.ABCMeta):
    """
    """
    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, file, data_type):
        pass


class ReconstructOrderBookHandler(Handler):
    """
    Handle request
    """

    def handle_request(self, file, data_type):
        """
        :param file: Data file
        :param data_type: Message data or Order Data
        :return: A series of order books
        """
        if True:
            limit_order_book = LimitOrderBook()

            if data_type == 'message':
                data_reader = MessageDataReader()
            elif data_type == 'order':
                data_reader = OrderBookDataReader()
            else:
                raise NotImplementedError('Data type not recognised')

            data_reader.read_data(file)
            lob_updater = LimitOrderBookUpdater(data_reader.messages)
            order_book_series = lob_updater.generate_books_from_message_data(limit_order_book)

            return order_book_series

        elif self._successor is not None:
            self._successor.handle_request(file, data_type)