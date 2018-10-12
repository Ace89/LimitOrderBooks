
import abc

from Analytics.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Factory.TimeSeriesFactory import TimeSeriesFactory
from Enums.TimeSeriesTypes import TimeSeriesTypes
from Analytics.EfficientPrice import EfficientPrice


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, file, data_type, start_time, end_time):
        pass


class EfficientPriceHandler(Handler):

    def handle_request(self, file, data_type, start_time, end_time):
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
            lob_updater.generate_books_from_message_data(limit_order_book)

            time_series_factory = TimeSeriesFactory(lob_updater.books)
            bid, ask = time_series_factory.create_time_series(TimeSeriesTypes.price, start_time=start_time,
                                                              time_interval=5)
            k = 150
            # what is this k
            eff_price = EfficientPrice(lob_updater)
            theta = eff_price.calculate_theta(k, start_time, end_time)
            price = eff_price.calculate_efficient_price(theta, bid)
            return price
        elif self._successor is not None:
            self._successor.handle_request(file, data_type, start_time, end_time)
