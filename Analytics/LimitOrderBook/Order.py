"""
    Aim:
        Outline Order class

        Order types
        1: Submission of a new limit order
        2: Cancellation (Partial deletion of a limit order) -> cannot exist on its own
        3: Deletion (Total deletion of a limit order) -> cannot exist on its own
        4: Execution of a visible limit order   -> cannot exist on its own
        5: Execution of a hidden limit order    -> cannot exist on its own their order id will be 0 in the data
        7: Trading halt indicator

        Execution type and Visibility are redundant at the moment
"""

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"


class Order:

    def __init__(self, submission_time, order_type, order_id, size, price, direction):

        #if type(order_type) is not type(OrderType):
          #  raise Exception('order type should be of type Enums.OrderType')

        self.submission_time = submission_time
        self.order_type = order_type
        self.order_id = order_id
        self.size = size
        self.price = price
        self.direction = direction
        self.remaining_size = size

    def __hash__(self):
        return self.submission_time + self.size + self.price + self.direction

    def __lt__(self, order):
        if self.price != order.price:
            return self.price < order.price

        return self.submission_time > order.submission_time

    def __gt__(self, order):
        if self.price != order.price:
            return self.price > order.price

        return self.submission_time < order.submission_time

    def __eq__(self, order):
        return self.order_id == order.order_id
