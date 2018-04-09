#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class OrderBookTree:

    @staticmethod
    def __doc__():
        return "contains number of levels of interest in the order book, dictionaries for prices " \
               "and list of volumes for that price"

    def __init__(self, start_time, end_time, buy_levels, sell_levels, levels=3):
        """
        :param start_time: time of first order
        :param end_time: time of last order
        :param buy_levels: dictionary of buy prices and their volumes
        :param sell_levels: dictionary of sell prices and their volumes
        :param levels: Number of relevant price levels
        """
        self.start_time = start_time
        self.end_time = end_time
        self.levels = levels
        self.buy_levels = buy_levels
        self.sell_levels = sell_levels