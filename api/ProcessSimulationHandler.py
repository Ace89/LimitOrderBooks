
import abc

from Analytics.HawkesProcess import HawkesProcess


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, intensity, events, alpha, beta, l):
        pass


class HawkesProcessSimulation(Handler):

    def handle_request(self, intensity, events, alpha, beta, l):
        if True:
            hawkes = HawkesProcess(intensity)
            time_series = hawkes.simulate_process(events, alpha, beta, l)
            return time_series
        elif self._successor is not None:
            self._successor.handle_request(intensity, events, alpha, beta, l)