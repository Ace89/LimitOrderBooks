
from abc import ABC, abstractmethod


class INonLinearModel(ABC):

    @abstractmethod
    def fit_data(self, time_series):
        raise NotImplementedError('This method has not been implemented')
