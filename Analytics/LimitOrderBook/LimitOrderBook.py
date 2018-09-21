
#from Analytics.LimitOrderBook.Queue import Queue
from Analytics.LimitOrderBook.NestedQueue import NestedQueue
import numpy as np


class LimitOrderBook:

    def __init__(self):
        #self.bid_queue = Queue()
        #self.ask_queue = Queue()
        self.bid_queue = NestedQueue()
        self.ask_queue = NestedQueue()

    def get_bid_price_size(self, levels):
        output = list()
        for point in self.bid_queue.queue:
            size = 0
            for order in point.queue:
                size += order.size
            output.append((point.queue[0].price, size))

        output.sort(key=lambda tup: tup[0], reverse=True)

        return output[0:levels]

    def get_ask_price_size(self, levels):
        output = list()
        for point in self.ask_queue.queue:
            size = 0
            for order in point.queue:
                size += order.size
            output.append((point.queue[0].price, size))

        output.sort(key=lambda tup: tup[0])

        return output[0:levels]

    def get_best_bid(self):
        return self.bid_queue.get_top()

    def get_best_ask(self):
        return self.ask_queue.get_top()

    # introduce a plot method here
