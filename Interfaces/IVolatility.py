
from abc import ABC, abstractmethod


class IVolatility(ABC):

    @abstractmethod
    def calculate_volatility(self):
        raise NotImplementedError

