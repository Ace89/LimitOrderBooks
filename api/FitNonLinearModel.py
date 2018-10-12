
import abc

from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Analytics.GARCHModel import GARCHModel


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, model, time_series):
        pass


class FitNonLinearModel(Handler):

    def handle_request(self, model, time_series):

        if True:
            if isinstance(time_series, LimitOrderBookSeries) is False:
                return NotImplementedError('time series type not recognised')

            if model is not 'garch':
                raise NotImplementedError('Model not recognised')

            non_lin_model = GARCHModel()
            return non_lin_model.fit_data(time_series)
        elif self._successor is not None:
            self._successor.handle_request(model, time_series)
