
import abc

from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.ExtractPrices import ExtractPrices
from sklearn import svm

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, file):
        pass


class PriceForecastHandler(Handler):

    def handle_request(self, file):
        if True:
            data_reader = OrderBookDataReader()
            data = data_reader.read_data(file)
            extract_prices = ExtractPrices()
            x, y = extract_prices.extract_data(data)
            clf = svm.SVC()
            clf.fit(x[0:990], y[0:990])
            output = []
            for i in range(991, 999):
                prediction = clf.predict(x[i])
                output.append(prediction[0])

            return output
        elif self._successor is not None:
            self._successor.handle_request(file)