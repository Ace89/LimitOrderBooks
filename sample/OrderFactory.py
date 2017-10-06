"""
Aim: Create an order factory

"""

from sample.Order import Order, OrderType


class OrderFactory:

    def __init__(self):
        pass

    @staticmethod
    def create_order(submission_time,
                     direction,
                     price,
                     volume,
                     visibility,
                     order_type):

            return Order(submission_time, direction, price, volume, visibility, OrderType(order_type))


