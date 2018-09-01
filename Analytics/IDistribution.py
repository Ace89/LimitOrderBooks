
from abc import ABC, abstractmethod


class IDistribution(ABC):

    @abstractmethod
    def fit_data(self,
                 time_series):
        raise NotImplementedError('This is an abstract method')