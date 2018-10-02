
from Analytics.LimitOrderBook.Order import Order
from Analytics.LimitOrderBook.Queue import Queue
from Analytics.LimitOrderBook.DataReaderResult import DataReaderResult
from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType


class LimitOrderBookUpdater:

    def __init__(self, messages, order_book_data):
        self.messages = messages
        self.order_book_data = order_book_data

    def generate_order_book_series_from_message_data(self, limit_order_book):
        books = list()
        time_series_idx = list()

        if len(limit_order_book.ask_queue.queue) ==0 and len(limit_order_book.bid_queue.queue) ==0:
            self.update_empty_order_book(limit_order_book)

        for order in self.messages:
            if order.direction == OrderDirection.Buy:
                if order.order_type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
                else:
                    limit_order_book.bid_queue.dequeue(order)
            else:
                if order.order_type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)
                else:
                    limit_order_book.ask_queue.dequeue(order)
            time = order.submission_time
            bid = Queue()
            ask = Queue()
            bid.queue = [val for val in limit_order_book.bid_queue.queue]
            ask.queue = [val for val in limit_order_book.ask_queue.queue]
            data_reader_result = DataReaderResult(time, bid, ask)
            time_series_idx.append(time)
            books.append(data_reader_result)

        return LimitOrderBookSeries(books, time_series_idx)

    def update_empty_order_book(self, limit_order_book):
        # this is for the case that the limit order book is empty
        time = 34200

        existing_orders = list()

        bid_price_columns = list(filter(lambda x: 'BidPrice' in x, self.order_book_data.columns))
        bid_size_columns = list(filter(lambda x: 'BidSize' in x, self.order_book_data.columns))
        ask_price_columns = list(filter(lambda x: 'AskPrice' in x, self.order_book_data.columns))
        ask_size_columns = list(filter(lambda x: 'AskSize' in x, self.order_book_data.columns))

        row = self.order_book_data.iloc[0]
        id = 0
        for ask_p, ask_s in zip(ask_price_columns, ask_size_columns):
            id += 1
            existing_orders.append(Order(time, OrderType.Submission, id, row[ask_s], row[ask_p], OrderDirection.Sell))

        for bid_p, bid_s in zip(bid_price_columns, bid_size_columns):
            id += 1
            existing_orders.append(Order(time, OrderType.Submission, id, row[bid_s], row[bid_p], OrderDirection.Buy))
        """
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
        """
        for order in existing_orders:
            if order.direction == OrderDirection.Buy:
                if order.order_type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
            else:
                if order.order_type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)

        return None

    def generate_order_book_series_from_order_book_data(self, limit_order_book):

        bid_price_columns = list(filter(lambda x: 'BidPrice' in x, self.order_book_data.columns))
        bid_size_columns = list(filter(lambda x: 'BidSize' in x, self.order_book_data.columns))
        ask_price_columns = list(filter(lambda x: 'AskPrice' in x, self.order_book_data.columns))
        ask_size_columns = list(filter(lambda x: 'AskSize' in x, self.order_book_data.columns))

        books = list()
        times = self.order_book_data['Time']
        for idx in range(0, len(self.order_book_data)):
            # for each row in the order book data populate bid/ask queues with orders
            row = self.order_book_data.iloc[idx]

            for ask_p, ask_s in zip(ask_price_columns, ask_size_columns):
                limit_order_book.ask_queue.queue.append(Order(row['Time'], OrderType.Submission, 0, row[ask_s], row[ask_p], OrderDirection.Sell))

            for bid_p, bid_s in zip(bid_price_columns, bid_size_columns):
                limit_order_book.bid_queue.queue.append(Order(row['Time'], OrderType.Submission, 0, row[bid_s], row[bid_p], OrderDirection.Buy))
            """
            for ticker in bid_tickers:
                limit_order_book.bid_queue.queue.append((self.order_book_data.iloc[idx][ticker[0]],
                                                         self.order_book_data.iloc[idx][ticker[1]]))

            for ticker in ask_tickers:
                limit_order_book.ask_queue.queue.append((self.order_book_data.iloc[idx][ticker[0]],
                                                         self.order_book_data.iloc[idx][ticker[1]]))
            """

            bid = Queue()
            ask = Queue()
            bid.queue = [val for val in limit_order_book.bid_queue.queue]
            ask.queue = [val for val in limit_order_book.ask_queue.queue]

            data_reader_result = DataReaderResult(row['Time'], bid, ask)
            books.append(data_reader_result)

        return LimitOrderBookSeries(books, times)

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
