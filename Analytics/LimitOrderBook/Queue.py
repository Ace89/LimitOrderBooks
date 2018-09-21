
# https://www.pythoncentral.io/use-queue-beginners-guide/


class Queue:

    def __init__(self):
        self.queue = list()

    def enqueue(self, item):

        if len(self.queue) == 0:
            self.queue.append(item)
            return

        smaller_orders = list(filter(lambda x: x < item, self.queue))
        larger_orders = list(filter(lambda x: x > item, self.queue))

        self.queue = smaller_orders + [item] + larger_orders
        return

    def dequeue(self, item):

        for order in self.queue:
            if order == item:
                order.size -= item.size
                if order.size == 0:
                    self.queue.remove(order)

        return

    def size(self):
        return len(self.queue)

    def get_top(self):
        return self.queue[-1]
