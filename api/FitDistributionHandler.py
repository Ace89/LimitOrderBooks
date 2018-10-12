
import abc

from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Analytics.StudentTDistribution import StudentTDistribution


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, time_series, distribution):
        pass


class FitDistributionHandler(Handler):

    def handle_request(self, time_series, distribution):
        if True:
            if isinstance(time_series, LimitOrderBookSeries) is False:
                raise NotImplementedError('Time series type not recognised')

            if distribution == 'students-t':
                dist = StudentTDistribution()
            else:
                raise NotImplementedError('This distribution is not supported')

            return dist.fit_data(time_series)
        elif self._successor is not None:
            self._successor.handle_request(time_series, distribution)