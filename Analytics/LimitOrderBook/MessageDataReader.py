
from Analytics.LimitOrderBook.DataReader import DataReader
from Analytics.LimitOrderBook.Message import Message
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection


class MessageDataReader(DataReader):

    def __init__(self):
        self.messages = list()

    def read_data(self, message_file):
        import pandas as pd

        messages = pd.read_csv(message_file)

        for msg in messages.index:
            message = Message(messages['Time'][msg],
                              OrderType(messages['Type'][msg]),
                              messages['OrderId'][msg],
                              messages['Size'][msg],
                              messages['Price'][msg],
                              OrderDirection(messages['Direction'][msg]))
            self.messages.append(message)
