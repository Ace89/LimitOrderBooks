
from abc import ABC, abstractmethod


class INonLinearModel(ABC):

    @abstractmethod
    def fit_data(self, data):
        raise NotImplementedError
