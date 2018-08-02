
from Analytics.LimitOrderBook.Message import Message


class MessageDataReader:

    def __init__(self):
        self.messages = list()

    def read_messages(self, message_file):
        import pandas as pd

        messages = pd.read_csv(message_file)

        for msg in messages.index:
            message = Message(messages['Time'][msg], messages['Type'][msg], messages['OrderId'][msg],
                              messages['Size'][msg], messages['Price'][msg], messages['Direction'][msg])
            self.messages.append(message)
