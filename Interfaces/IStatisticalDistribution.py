
from abc import ABC, abstractmethod


class IStatisticalDistribution(ABC):

    @abstractmethod
    def fit_data(self, time_series):
        raise NotImplementedError
