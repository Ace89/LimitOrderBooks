
from abc import ABC, abstractmethod


class ILinearModel(ABC):

    @abstractmethod
    def fit_data(self, x, y):
        raise NotImplementedError('This method has not been implemented')