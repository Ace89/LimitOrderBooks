"""
    Aim:
        Create a string of prices to represent bids and offers
"""

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']


class PriceLevel:

    def __init__(self, price):
        self.price = price
        self.next_level = None
        self.volumes = []

    def __lt__(self, other):
        if self.price < other.get_price():
            return True
        else:
            return False

    def __le__(self, other):
        if self.price <= other.get_price():
            return True
        else:
            return False

    def __gt__(self, other):
        if self.price > other.get_price():
            return True
        else:
            return False

    def __ge__(self, other):
        if self.price <= other.get_price():
            return False
        else:
            return True

    def __eq__(self, other):
        if self.price == other.get_price():
            return True
        else:
            return False

    def set_next_price(self,bid_price):
        self.next_level = bid_price

    def get_next_price(self):
        return self.next_level

    def add_volume(self, volume):
        self.volumes.append(volume)

    def get_volumes(self):
        return self.volumes

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price
