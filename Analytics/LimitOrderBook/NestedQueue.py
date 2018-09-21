
from Analytics.LimitOrderBook.Queue import Queue


class NestedQueue:

    def __init__(self):
        self.queue = Queue()

    def enqueue(self, item):

        if self.queue.size() == 0:
            self.queue.enqueue(item)
            return

        for price_queue in self.queue.queue:
            if price_queue.price == item.price:
                self.queue.enqueue(item)
                return

        self.queue.enqueue(item)
        return

    def dequeue(self, item):

        for price_queue in self.queue.queue:
            if price_queue.price == item.price:
                price_queue.dequeue(item)
                if len(price_queue.queue) == 0:
                    self.queue.dequeue(price_queue)
                return

        return