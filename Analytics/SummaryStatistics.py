
from Analytics.SummaryStatisticsResult import SummaryStatisticsResult
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection

import numpy as np


class SummaryStatistics:

    def __init__(self, message_data):
        """
        :param message_data: message data
        """
        self.message_data = message_data

    def number_order_buy_sell(self, order_type=OrderType.Submission, order_direction=OrderDirection.Buy):
        message_data = list(filter(lambda x: x.type == order_type, self.message_data))
        number_order = len(list(filter(lambda x: x.direction == order_direction, message_data)))
        return number_order

    def number_deletion_buy_sell(self):
        message_data = list(filter(lambda x: x.type == OrderType.Deletion, self.message_data))
        number_order_buy = len(list(filter(lambda x: x.direction == OrderDirection.Buy, message_data)))
        number_order_sell = len(list(filter(lambda x: x.direction == OrderDirection.Sell, message_data)))
        return number_order_buy, number_order_sell

    def number_trades(self):
        message_data = list(filter(lambda x: x.type == OrderType.VisibleExecution or x.type == OrderType.HiddenExecution,
                                   self.message_data))
        return len(message_data)

    def number_trades_buy_sell(self, order_direction=OrderDirection.Buy):
        message_data = list(filter(lambda x: x.type == OrderType.Submission or x.type == OrderType.HiddenExecution,
                                   self.message_data))
        number_order = len(list(filter(lambda x: x.direction == order_direction, message_data)))
        return number_order

    def price_order_buy_sell(self, order_type=OrderType.Submission, order_direction=OrderDirection.Buy):
        message_data = list(filter(lambda x: x.type == order_type, self.message_data))
        message_data = list(filter(lambda x: x.direction == order_direction, message_data))
        prices = [message.price for message in message_data]
        return prices

    def price_trades(self):
        message_data = list(filter(lambda x: x.type == OrderType.Submission or x.type == OrderType.HiddenExecution,
                                   self.message_data))
        prices = [message.price for message in message_data]
        return prices

    def size_order_buy_sell(self, order_type=OrderType.Submission, order_direction=OrderDirection.Buy):
        message_data = list(filter(lambda x: x.type == order_type, self.message_data))
        message_data = list(filter(lambda x: x.direction == order_direction, message_data))
        size = [message.size for message in message_data]
        return size

    def size_trades(self):
        message_data = list(filter(lambda x: x.type == OrderType.Submission or x.type == OrderType.HiddenExecution,
                                   self.message_data))
        size = [message.size for message in message_data]
        return size

    def generate_summary(self):

        buy_order_prices = self.price_order_buy_sell()
        sell_order_prices = self.price_order_buy_sell(OrderType.Submission, OrderDirection.Sell)
        buy_delete_prices = self.price_order_buy_sell(OrderType.Deletion, OrderDirection.Buy)
        sell_delete_prices = self.price_order_buy_sell(OrderType.Deletion, OrderDirection.Sell)
        trade_prices = self.price_trades()

        buy_order_sizes = self.size_order_buy_sell()
        sell_order_sizes = self.size_order_buy_sell(OrderType.Submission, OrderDirection.Sell)
        buy_delete_sizes = self.size_order_buy_sell(OrderType.Deletion, OrderDirection.Buy)
        sell_delete_sizes = self.size_order_buy_sell(OrderType.Deletion, OrderDirection.Sell)
        trade_sizes = self.size_trades()

        summary_stats_result = SummaryStatisticsResult(self.message_data[0].time,
                                                       self.message_data[-1].time,
                                                       self.number_order_buy_sell(),
                                                       self.number_order_buy_sell(OrderType.Submission, OrderDirection.Sell),
                                                       self.number_order_buy_sell(OrderType.Deletion, OrderDirection.Buy),
                                                       self.number_order_buy_sell(OrderType.Deletion, OrderDirection.Sell),
                                                       self.number_trades(),
                                                       self.number_trades_buy_sell(),
                                                       self.number_trades_buy_sell(OrderDirection.Sell),
                                                       np.average(buy_order_prices),
                                                       np.average(sell_order_prices),
                                                       np.average(buy_delete_prices),
                                                       np.average(sell_delete_prices),
                                                       np.average(trade_prices),
                                                       np.std(buy_order_prices),
                                                       np.std(sell_order_prices),
                                                       np.std(buy_delete_prices),
                                                       np.std(sell_delete_prices),
                                                       np.std(trade_prices),
                                                       np.median(buy_order_prices),
                                                       np.median(sell_order_prices),
                                                       np.median(buy_delete_prices),
                                                       np.median(sell_delete_prices),
                                                       np.median(trade_prices),
                                                       np.average(buy_order_sizes),
                                                       np.average(sell_order_sizes),
                                                       np.average(buy_delete_sizes),
                                                       np.average(sell_delete_sizes),
                                                       np.average(trade_sizes),
                                                       np.std(buy_order_sizes),
                                                       np.std(sell_order_sizes),
                                                       np.std(buy_delete_sizes),
                                                       np.std(sell_delete_sizes),
                                                       np.std(trade_sizes),
                                                       np.median(buy_order_sizes),
                                                       np.median(sell_order_sizes),
                                                       np.median(buy_delete_sizes),
                                                       np.median(sell_delete_sizes),
                                                       np.median(trade_sizes))
        return summary_stats_result
