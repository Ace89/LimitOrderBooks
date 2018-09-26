
from abc import ABC, abstractmethod


class IDataReader(ABC):
    @abstractmethod
    def read_data(self, message_file):
        raise NotImplementedError('This method is not implemented')
