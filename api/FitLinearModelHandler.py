
import abc

from Analytics.LinearRegression import LinearRegression
from Analytics.LogisticRegression import LogisticRegression


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor=successor

    @abc.abstractmethod
    def handle_request(self, model_name, x, y):
        pass


class FitLinearModelHandler(Handler):

    def handle_request(self, model_name, x, y):

        if True:
            if model_name == 'linear':
                model = LinearRegression()
                return model.fit_data(x, y)
            elif model_name == 'logistic':
                model = LogisticRegression()
                return model.fit_data(x, y)
            else:
                raise NotImplementedError('Model not recognised')
        elif self._successor is not None:
            self._successor.handle_request(model_name, x, y)