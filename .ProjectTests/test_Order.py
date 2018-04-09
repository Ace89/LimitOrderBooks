"""

"""

from sample.OrderFactory import OrderFactory
from sample.Order import Order, Direction, Visibility, ExecutionType, OrderType

import unittest


class TestOrder(unittest.TestCase):

    def __init__(self):
        pass
"""
    def test_limit_order_creation(self): only limit orders
        order_factory = OrderFactory()
        limit_order = order_factory.create_order('Limit', '', '', Direction.Bid, 100.0, 1000, Visibility.Visible)
        self.assertTrue(type(limit_order) == LimitOrder)

    def test_market_order_creation(self):
        order_factory = OrderFactory()
        limit_order = order_factory.create_order('Market', '', '', Direction.Bid, 100.0, 1000, Visibility.Visible)
        self.assertTrue(type(limit_order) == MarketOrder)
"""

if __name__ == '__main__':
    unittest.main()
