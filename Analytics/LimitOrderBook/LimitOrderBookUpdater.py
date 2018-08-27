
import numpy as np

from Analytics.LimitOrderBook.Order import Order
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType
from Enums.TimeSeriesTypes import TimeSeriesTypes
from Factory.TimeSeriesFactory import TimeSeriesFactory


class LimitOrderBookUpdater:

    def __init__(self, messages):
        self.messages = messages
        self.books = None

    def update_order_book(self, limit_order_book):
        books = list()

        for message in self.messages:
            order = Order(message.time, message.type, message.order_id,
                          message.size, message.price, message.direction)
            if message.direction == OrderDirection.Buy:
                if message.type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
                else:
                    limit_order_book.bid_queue.dequeue(order)
            else:
                if message.type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)
                else:
                    limit_order_book.ask_queue.dequeue(order)
            books.append((limit_order_book.bid_queue.queue, limit_order_book.ask_queue.queue))

        self.books = books

    def create_time_series(self, start_time=34200, time_interval=5, series_type=TimeSeriesTypes.price):
        """
        :param start_time: start time
        :param time_interval: time interval
        :param series_type: series type
        :return: time series
        """
        time_series_factory = TimeSeriesFactory(self.books)
        return time_series_factory.create_time_series(series_type, start_time, time_interval)

    def number_of_limit_order(self, order_type=OrderType.Submission, start_time=34200, end_time=57600):
        """
        :param order_type: order type
        :param start_time: start time
        :param end_time: end time
        :return: number of limit orders
        """
        if order_type is not None:
            limit_orders = list(filter(lambda x: x.type == order_type, self.messages))
            limit_orders = list(filter(lambda x: start_time <= x.time <= end_time, limit_orders))
        else:
            limit_orders = list(filter(lambda x: start_time <= x.time <= end_time, self.messages))

        return len(limit_orders)

    def calculate_efficient_price(self, k=150, start_time=34200, end_time=34340):
        # calculate mu
        # then h(y_t)
        # then invert h(y_t)
        T = end_time-start_time
        n = self.number_of_limit_order(OrderType.Submission,start_time, end_time)
        mu = n/T
        theta = list()
        for i in range(1, k+1):
            orders = self.number_of_limit_order(OrderType.Submission,start_time + (i-1)*T/k, start_time + (i-1)*T/k + (6/7.15))
            theta.append(orders/(n/k))

        theta = np.sort(theta)

        return theta