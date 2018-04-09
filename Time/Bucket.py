
import datetime

"""
Designed to break up time intervals into buckets
"""


class Bucket:

    def __init__(self, start_time, end_time):
        """
        :param start_time: start time of bucket
        :param end_time: end time of bucket
        :param price: market price, can be a single value, or an array
        :param volume: market volume
        """
        if type(start_time) != datetime.datetime:
            raise Exception("Start time must be of type datetime.time")

        if type(end_time) != datetime.datetime:
            raise Exception("End time must of type datetime.time")

        self.start_time = start_time
        self.end_time = end_time
        self.price = None
        self.volume = None
        self.buy_orders = None
        self.sell_orders = None

    def set_price(self, price):
        """
        :param price: can be a single value or an array
        :return: none
        """
        self.price = price

    def set_volume(self, volume):
        """
        :param volume: can be a single value or an array
        :return: none
        """
        self.volume = volume
