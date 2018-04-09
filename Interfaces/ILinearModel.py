
from abc import ABC, abstractmethod


class ILinearModel(ABC):

    @abstractmethod
    def fit_data(self, time_series_x, time_series_y):
        raise NotImplementedError
