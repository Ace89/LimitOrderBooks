
from Analytics.LimitOrderBook.IDataReader import IDataReader
from Analytics.LimitOrderBook.Message import Message
from Analytics.LimitOrderBook.Order import Order
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection

import pandas as pd

class MessageDataReader(IDataReader):

    def __init__(self):
        self.messages = None
        self.message_file = None
        self.msg_frame = None
        self.columns = ['Time', 'Type', 'OrderId', 'Size', 'Price', 'Direction']

    def read_data(self, message_file):
        # check if request already made
        if self.messages is not None and self.message_file == message_file:
            return self.messages
        else:
            self.message_file = message_file
            self.messages = list()

            messages = pd.read_csv(message_file)
            messages.columns = self.columns

            for i in range(0, len(messages)):
                msg = messages.iloc[i]
                order = Order(msg['Time'],
                              OrderType(msg['Type']),
                              msg['OrderId'],
                              msg['Size'],
                              msg['Price'],
                              OrderDirection(msg['Direction']))
                self.messages.append(order)
            return self.messages

    def read_data_frame(self, message_file):
        if self.msg_frame is not None and self.message_file == message_file:
            return self.msg_frame
        else:
            self.msg_frame = pd.read_csv(message_file)
            self.msg_frame.columns = self.columns
            return self.msg_frame


