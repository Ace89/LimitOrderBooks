
from Analytics.LimitOrderBook.Order import Order
from Analytics.LimitOrderBook.DataReaderResult import DataReaderResult
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType


class LimitOrderBookUpdater:

    def __init__(self, messages):
        self.messages = messages
        self.order_book_data = None
        self.books = None

    def add_order_book_data(self, order_book_data):
        self.order_book_data = order_book_data

    def update_order_book(self, limit_order_book):
        books = list()
        levels = 5
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
            #bid_price_size = limit_order_book.get_bid_price_size(levels)
            #ask_price_size = limit_order_book.get_ask_price_size(levels)
            data_reader_result = DataReaderResult(message.time,
                                                  limit_order_book.bid_queue,
                                                  limit_order_book.ask_queue)
            books.append(data_reader_result)
            #books.append((message.time, (bid_price_size, ask_price_size)))

        self.books = books

    @staticmethod
    def update_empty_order_book(limit_order_book):
        # this is for the case that the limit order book is empty
        time = 34200
        existing_orders = list()
        existing_orders.append(Order(time, OrderType.Submission, 1, 100, 2239500, OrderDirection.Sell))
        existing_orders.append(Order(time, OrderType.Submission, 2, 100, 2239900, OrderDirection.Sell))
        existing_orders.append(Order(time, OrderType.Submission, 3, 220, 2240000, OrderDirection.Sell))
        existing_orders.append(Order(time, OrderType.Submission, 4, 100, 2242500, OrderDirection.Sell))
        existing_orders.append(Order(time, OrderType.Submission, 5, 547, 2244000, OrderDirection.Sell))
        existing_orders.append(Order(time, OrderType.Submission, 6, 100, 2231800, OrderDirection.Buy))
        existing_orders.append(Order(time, OrderType.Submission, 7, 200, 2230700, OrderDirection.Buy))
        existing_orders.append(Order(time, OrderType.Submission, 8, 100, 2230400, OrderDirection.Buy))
        existing_orders.append(Order(time, OrderType.Submission, 9, 10, 2230000, OrderDirection.Buy))
        existing_orders.append(Order(time, OrderType.Submission, 10, 100, 2226200, OrderDirection.Buy))

        for order in existing_orders:
            if order.direction == OrderDirection.Buy:
                if order.order_type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
                else:
                    limit_order_book.ask_queue.dequeue(order)
            else:
                if order.order_type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)
                else:
                    limit_order_book.bid_queue.dequeue(order)

        None

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
