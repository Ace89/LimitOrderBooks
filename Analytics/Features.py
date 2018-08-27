
from abc import ABC, abstractmethod


class Features(ABC):
    @abstractmethod
    def extract_data(self, data):
        pass
