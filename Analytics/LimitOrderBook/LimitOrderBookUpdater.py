
from Analytics.LimitOrderBook.Order import Order
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType


class LimitOrderBookUpdater:

    def __init__(self):
        self.books = None

    def update_order_book(self, limit_order_book, messages):
        books = list()
        for message in messages:
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

    def create_time_series(self, start_time=34200, time_interval=5):
        bid_price = list()
        bid_volume = list()
        ask_price = list()
        ask_volume = list()
        for book in self.books:
            if book[0][-1].submission_time > start_time:
                bid_price.append(book[0][-1].price)
                bid_volume.append(book[0][-1].size)
                ask_price.append(book[1][0].price)
                ask_volume.append(book[1][0].size)
                start_time += time_interval

        return bid_price, bid_volume, ask_price, ask_volume

