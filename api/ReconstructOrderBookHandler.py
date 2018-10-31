
import abc
from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookBuilder


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

    def handle_request(self, order_file, message_data_file, data_type):
        """
        :param order_file: Order data file
        :param message_data_file: Message data file
        :param data_type: Message data or Order Data
        :return: A series of order books
        """
        if True:
            limit_order_book = LimitOrderBook()

            msg_data_reader = MessageDataReader()
            order_data_reader = OrderBookDataReader(5, message_data_file)

            msg_data = msg_data_reader.read_data(message_data_file)
            order_data = order_data_reader.read_data(order_file)

            lob_builder = LimitOrderBookBuilder(msg_data, order_data, limit_order_book)
            order_book_series = lob_builder.build(data_type)

            return order_book_series

        elif self._successor is not None:
            self._successor.handle_request(order_file, message_data_file, data_type)
