
import abc

from Enums.TimeSeriesTypes import TimeSeriesTypes
from Factory.TimeSeriesFactory import TimeSeriesFactory


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, time_series_type, limit_order_books, start_time, interval):
        pass


class GenerateTimeSeriesRequestHandler(Handler):

    def handle_request(self, time_series_type, limit_order_books, start_time, interval):
        if True:
            time_series = TimeSeriesTypes(time_series_type)
            time_series_factory = TimeSeriesFactory(limit_order_books)
            output = time_series_factory.create_time_series(time_series, start_time, interval)
            return output
        elif self._successor is not None:
            self._successor.handle_request(time_series_type, limit_order_books, start_time, interval)
