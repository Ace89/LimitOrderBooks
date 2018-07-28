"""

# keys will be Queue level and values will be list of tuples
# Queue level corresponds to a price

"""


class OrderQueue:

    def __init__(self, order_queue_type):
        self.order_queue_type = order_queue_type
        self.orders = dict()
