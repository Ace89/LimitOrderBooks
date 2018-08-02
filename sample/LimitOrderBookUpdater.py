
from sample.LimitOrderBook import LimitOrderBook
from Data.MessageDataReader import MessageDataReader

from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType
from sample.Order import Order


class LimitOrderBookUpdater:

    def __init__(self):
        self.books = None

    def update_order_book(self, limit_order_book, messages):
        #best_bid = list()
        #best_ask = list()
        books = list()
        for message in messages:
            order = Order(message.time, message.type, message.order_id,
                          message.size, message.price, message.direction)
            if message.direction == OrderDirection.Buy:
                if message.type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
                else:
                    limit_order_book.bid_queue.dequeue(order)
            else:
                if message.type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)
                else:
                    limit_order_book.ask_queue.dequeue(order)
            books.append((limit_order_book.bid_queue.queue, limit_order_book.ask_queue.queue))
            #if len(limit_order_book.bid_queue.queue) > 0:
            #    best_bid.append(limit_order_book.bid_queue.queue[-1].price)
            #if len(limit_order_book.ask_queue.queue) > 0:
            #    best_ask.append(limit_order_book.ask_queue.queue[0].price)
        self.books = books

    def create_time_series(self):
        bid_price = list()
        bid_volume = list()
        ask_price = list()
        ask_volume =  list()
        for book in self.books:
            bid_price.append(book[0][-1].price)
            bid_volume.append(book[0][-1].size)
            ask_price.append(book[1][0].price)
            ask_volume.append(book[1][0].size)

        return bid_price, bid_volume, ask_price, ask_volume

if __name__ == '__main__':
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'

    lob = LimitOrderBook()
    msgDataReader = MessageDataReader()
    lob_updater = LimitOrderBookUpdater()

    start = time.time()

    msgDataReader.read_messages(file_path+file_name)
    lob_updater.update_order_book(lob, msgDataReader.messages)

    bid_price, bid_volume, ask_price, ask_volume = lob_updater.create_time_series()

    bid = np.asarray(bid_price)
    ask = np.asarray(ask_price)

    plt.subplot(4, 1, 1)
    plt.plot(bid/10000)
    plt.title('Bid')

    plt.subplot(4, 1, 3)
    plt.plot(ask/10000)
    plt.title('Ask')

    plt.show()

    end = time.time()
