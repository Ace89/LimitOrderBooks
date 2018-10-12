
import abc

from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.SummaryStatistics import SummaryStatistics


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, file, data_type):
        pass


class SummaryStatisticsHandler(Handler):

    def handle_request(self, file, data_type):
        if True:
            if data_type == 'message':
                data_reader = MessageDataReader()
            else:
                raise NotImplementedError('Data type not recognised')

            data_reader.read_data(file)

            summary = SummaryStatistics(data_reader.messages)

            return summary.generate_summary()
        elif self._successor is not None:
            self._successor.handle_request(file, data_type)