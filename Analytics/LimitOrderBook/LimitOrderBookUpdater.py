
from Analytics.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.Order import Order
from Analytics.LimitOrderBook.Queue import Queue
from Analytics.LimitOrderBook.DataReaderResult import DataReaderResult
from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType
import abc


class LimitOrderBookUpdater:

    def __init__(self, messages, order_book_data):
        self.messages = messages
        self.order_book_data = order_book_data

    def generate_order_book_series(self, data_type='order_book'):
        """
        :param data_type: message data or order book data
        :return: order book series
        """
        """
        To create an order book series using message data, the order book data is 
        also required to obtain the starting state of the bid and ask queues
        
        An order book series can be created solely from order book data
        """
        lob = LimitOrderBook()
        if data_type is 'messages' and self.order_book_data is not None:
            series = self.generate_books_from_message_data(lob)
            return series
        else:
            series = self.generate_books_from_order_book_data(lob)
            return series

    def generate_books_from_message_data(self, limit_order_book):
        books = list()
        time_series_idx = list()

        if len(limit_order_book.ask_queue.queue) == 0 and len(limit_order_book.bid_queue.queue) ==0:
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

    def generate_books_from_order_book_data(self, limit_order_book):

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
            # bid.queue = limit_order_book.bid_queue.queue.copy()
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
        """
        To be deleted once safely removed
        """

        if order_type is not None:
            limit_orders = list(filter(lambda x: x.type == order_type, self.messages))
            limit_orders = list(filter(lambda x: start_time <= x.time <= end_time, limit_orders))
        else:
            limit_orders = list(filter(lambda x: start_time <= x.time <= end_time, self.messages))

        return len(limit_orders)


class LimitOrderBookBuilder:

    def __init__(self, message_data, order_data, limit_order_book):
        self.message_data = message_data
        self.order_data = order_data
        self.limit_order_book = limit_order_book
        self.msg_data_builder = MessageDataOrderBookBuilder(message_data, order_data)
        self.order_data_builder = OrderDataOrderBookBuilder(order_data)
        """
        Also pass an instance of limit order book, if empty then fill using order data 
        if not then continue adding messages to lob 
        """
        
    def build(self, data_type='order_data'):
        if data_type is 'messages' and self.order_book_data is not None:
            series = self.msg_data_builder.build_order_book_series(self.limit_order_book)
            return series
        else:
            series = self.order_data_builder.build_order_book_series(self.limit_order_book)
            return series


class Builder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build_order_book_series(self, limit_order_book):
        pass


class MessageDataOrderBookBuilder(Builder):

    def __init__(self, message_data, order_data):
        self.message_data = message_data
        self.order_data = order_data

    def build_order_book_series(self, limit_order_book):
        books = list()
        time_series_idx = list()

        if len(limit_order_book.ask_queue.queue) == 0 and len(limit_order_book.bid_queue.queue) == 0:
            self._update_empty_order_book(limit_order_book)

        for order in self.messages_data:
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
            bid.queue = limit_order_book.bid_queue.queue.copy()
            ask.queue = limit_order_book.ask_queue.queue.copy()
            data_reader_result = DataReaderResult(time, bid, ask)
            time_series_idx.append(time)
            books.append(data_reader_result)

        return LimitOrderBookSeries(books, time_series_idx)

    def _update_empty_order_book(self, limit_order_book):
        # this is for the case that the limit order book is empty
        time = 34200

        existing_orders = list()

        bid_price_columns = list(filter(lambda x: 'BidPrice' in x, self.order_data.columns))
        bid_size_columns = list(filter(lambda x: 'BidSize' in x, self.order_data.columns))
        ask_price_columns = list(filter(lambda x: 'AskPrice' in x, self.order_data.columns))
        ask_size_columns = list(filter(lambda x: 'AskSize' in x, self.order_data.columns))

        row = self.order_data.iloc[0]
        id = 0
        for ask_p, ask_s in zip(ask_price_columns, ask_size_columns):
            id += 1
            existing_orders.append(Order(time, OrderType.Submission, id, row[ask_s], row[ask_p], OrderDirection.Sell))

        for bid_p, bid_s in zip(bid_price_columns, bid_size_columns):
            id += 1
            existing_orders.append(Order(time, OrderType.Submission, id, row[bid_s], row[bid_p], OrderDirection.Buy))

        for order in existing_orders:
            if order.direction == OrderDirection.Buy:
                if order.order_type == OrderType.Submission:
                    limit_order_book.bid_queue.enqueue(order)
            else:
                if order.order_type == OrderType.Submission:
                    limit_order_book.ask_queue.enqueue(order)

        return None


class OrderDataOrderBookBuilder(Builder):

    def __init__(self, order_data):
        self.order_data = order_data

    def build_order_book_series(self, limit_order_book):
        bid_price_columns = list(filter(lambda x: 'BidPrice' in x, self.order_data.columns))
        bid_size_columns = list(filter(lambda x: 'BidSize' in x, self.order_data.columns))
        ask_price_columns = list(filter(lambda x: 'AskPrice' in x, self.order_data.columns))
        ask_size_columns = list(filter(lambda x: 'AskSize' in x, self.order_data.columns))

        books = list()
        times = self.order_data['Time']
        for idx in range(0, len(self.order_data)):
            # for each row in the order book data populate bid/ask queues with orders
            row = self.order_data.iloc[idx]

            ask = Queue()
            bid = Queue()

            for ask_p, ask_s in zip(ask_price_columns, ask_size_columns):
                #limit_order_book.ask_queue.queue.append(Order(row['Time'], OrderType.Submission, 0, row[ask_s], row[ask_p], OrderDirection.Sell))
                ask.queue.append(Order(row['Time'], OrderType.Submission, 0, row[ask_s], row[ask_p], OrderDirection.Sell))

            for bid_p, bid_s in zip(bid_price_columns, bid_size_columns):
                #limit_order_book.bid_queue.queue.append(Order(row['Time'], OrderType.Submission, 0, row[bid_s], row[bid_p], OrderDirection.Buy))
                bid.queue.append(Order(row['Time'], OrderType.Submission, 0, row[bid_s], row[bid_p], OrderDirection.Buy))

            #bid = Queue()
            #ask = Queue()
            #bid.queue = limit_order_book.bid_queue.queue.copy()
            #ask.queue = limit_order_book.ask_queue.queue.copy()

            data_reader_result = DataReaderResult(row['Time'], bid, ask)
            books.append(data_reader_result)

        return LimitOrderBookSeries(books, times)
