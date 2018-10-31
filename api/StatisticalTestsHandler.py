
import abc

from Analytics.IStatisticalTest import IStatisticalTest
from Analytics.LimitOrderBookSeries import LimitOrderBookSeries


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, time_series, test):
        pass


class StatisticalTestsHandler(Handler):

    def handle_request(self, time_series, test):
        if isinstance(time_series, LimitOrderBookSeries) is False:
            raise NotImplementedError('Time series type not recognised')

        if True:
            stat_test = IStatisticalTest()

            if test == 'chow':
                return stat_test.chow_test()
            elif test == 'hurst':
                return stat_test.hurst_exponent(time_series)
            else:
                raise NotImplementedError('Test not recognised')
            pass
        elif self._successor is not None:
            self._successor.handle_request(time_series, test)