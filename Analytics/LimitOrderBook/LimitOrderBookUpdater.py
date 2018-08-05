
from Analytics.LimitOrderBook.Order import Order
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType


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

    def create_time_series(self, start_time=34200, time_interval=5, series_type='price'):
        
        if series_type == 'price':
            bid_output = list()
            ask_output = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    bid_output.append(book[0][-1].price)
                    ask_output.append(book[1][0].price)
                    start_time += time_interval
            return bid_output, ask_output
        elif series_type == 'size':
            bid_output = list()
            ask_output = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    bid_output.append(book[0][-1].size)
                    ask_output.append(book[1][0].size)
                    start_time += time_interval
            return bid_output, ask_output
        elif series_type == 'imbalance':
            imbalance_output = list()
            for book in self.books:
                if book[0][-1].submission_time > start_time:
                    imbalance_output.append(book[1][0].price - book[0][-1].price)
                    start_time += time_interval
            return imbalance_output
        else:
            raise NotImplementedError('series type not recognised')

    def number_of_limit_order(self, order_type=OrderType.Submission, start_time=34200, end_time=57600):
        limit_orders = list(filter(lambda x: x.type == order_type, self.messages))
        limit_orders = list(filter(lambda x: x.time >= start_time and x.time <= end_time, limit_orders))
        return len(limit_orders)
