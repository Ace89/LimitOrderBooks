
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection


class Message:

    def __init__(self, time, type, order_id, size, price, direction):
        self.time = time
        self.type = OrderType(type)
        self.order_id = order_id
        self.size = size
        self.price = price
        self.direction = OrderDirection(direction)
