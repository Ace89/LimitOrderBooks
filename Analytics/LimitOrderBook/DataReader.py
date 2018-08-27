
from abc import ABC, abstractmethod


class DataReader(ABC):
    @abstractmethod
    def read_data(self, message_file):
        pass
