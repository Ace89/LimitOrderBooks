
from Analytics.LimitOrderBook.Queue import Queue
#from Analytics.LimitOrderBook.NestedQueue import NestedQueue


class LimitOrderBook:

    def __init__(self):
        self.bid_queue = Queue()
        self.ask_queue = Queue()
        #self.bid_queue = NestedQueue()
        #self.ask_queue = NestedQueue()

    def get_bid_price_size(self):

        size = 0
        for order in self.bid_queue.queue:
            size += order.size

        return size

    def get_ask_price_size(self):
        size = 0
        for order in self.ask_queue.queue:
            size += order.size

        return size

    def get_best_bid(self):
        return self.bid_queue.get_top()

    def get_best_ask(self):
        return self.ask_queue.get_top()

    # introduce a plot method here
