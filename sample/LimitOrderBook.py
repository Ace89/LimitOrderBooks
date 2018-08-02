
from Data.Queue import Queue


class LimitOrderBook:

    def __init__(self):
        self.bid_queue = Queue()
        self.ask_queue = Queue()

    def get_best_bid(self):
        return self.bid_queue.get_top()

    def get_best_ask(self):
        return self.ask_queue.get_top()

    @classmethod
    def from_queues(cls, bid_queue, ask_queue):
        new_instance = cls()
        new_instance.bid_queue = bid_queue
        new_instance.ask_queue = ask_queue
        return new_instance
    # introduce a plot method here
