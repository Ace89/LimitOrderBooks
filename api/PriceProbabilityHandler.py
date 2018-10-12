
import abc

from api.ReconstructOrderBookHandler import ReconstructOrderBookHandler
from Factory.TimeSeriesFactory import TimeSeriesFactory
from Analytics.PriceForecast import PriceForecast

def reconstruct_order_book(file, data_type):
    """
    :param file: Data file
    :param data_type: Message data or Order data
    :return: A collection of books
    """
    order_book_handler = ReconstructOrderBookHandler()
    order_book_series = order_book_handler.handle_request(file, data_type)

    return order_book_series


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_Request(self, file, data_type):
        pass


class PriceProbabilityHandler(Handler):

    def handle_Request(self, file, data_type):
        if True:
            books = reconstruct_order_book(file, data_type)
            time_series_factory = TimeSeriesFactory(books)
            price_forecast = PriceForecast(time_series_factory)
            prob, freq = price_forecast.calculate_size_deciles()
            outputs = price_forecast.calibrate_hidden_liquidity_parameter()
            return price_forecast.calculate_probability_up_move
        elif self._successor is not None:
            self._successor.handle_request(file, data_type)