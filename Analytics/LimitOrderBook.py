
import pandas as pd
from Analytics.OrderQueue import OrderQueue
from Analytics.Order import Order
from Enums.OrderQueueType import OrderQueueType
from Enums.OrderDirection import OrderDirection
from Enums.OrderType import OrderType


"""
Only limit orders go into the queue

orders that are executed lead to an amendment in the orders in the queue
"""


class LimitOrderBook:

    def __init__(self, message_data):
        self.message_data = message_data.copy()
        self.events = len(self.message_data.index)

    def __build(self, time):

        message_data = self.message_data[self.message_data['Time'] <= time]
        bid_order_queue = OrderQueue(OrderQueueType.Bid)
        offer_order_queue = OrderQueue(OrderQueueType.Offer)

        for message in message_data.index:
            tmp_var = message_data['Direction'][message]
            order = Order(message_data['Time'][message],
                          OrderType(message_data['Type'][message]),
                          message_data['OrderId'][message],
                          message_data['Size'][message],
                          message_data['Price'][message],
                          OrderDirection(message_data['Direction'][message]))
            # have a case statement here

            if order.type == OrderType.Submission:
                if order.direction == OrderDirection.Buy:
                    if order.price not in bid_order_queue.orders.keys():
                        bid_order_queue.orders[order.price] = [(order.time, order.volume, order.id)]
                    else:
                        bid_order_queue.orders[order.price] = [bid_order_queue.orders[order.price]] + \
                                                              [(order.time, order.volume, order.id)]
                else:
                    if order.price not in offer_order_queue.orders.keys():
                        offer_order_queue.orders[order.price] = [(order.time, order.volume, order.id)]
                    else:
                        offer_order_queue.orders[order.price] = [bid_order_queue.orders[order.price]] + \
                                                                [(order.time, order.volume, order.id)]
            elif order.type == OrderType.Cancellation or order.type == OrderType.Visible_Execution:
                # go through the queues and partially cancel the order
                # order must be in the queues
                if order.direction == OrderDirection.Buy:
                    order_queue = bid_order_queue.orders[order.price]
                    for orders in order_queue:
                        if orders[2] == order.id:
                            orders[1] -= order.volume
                            if orders[1] == 0:
                                order_queue.remove(orders)
                else:
                    order_queue = offer_order_queue.orders[order.price]
                    for orders in order_queue:
                        if orders[2] == order[2]:
                            orders[1] -= order.volume
                            if orders[1] == 0:
                                order_queue.remove(orders)
                # order must exist in the queues
            elif order.type == OrderType.Deletion:
                # go through the queues and delete the order
                if order.direction == OrderDirection.Buy:
                    order_queue = bid_order_queue.orders[order.price]
                    for orders in order_queue:
                        if orders[2] == order.id:
                            order_queue.remove(orders)
                else:
                    order_queue = offer_order_queue.orders[order.price]
                    for orders in order_queue:
                        if orders[2] == order.id:
                            order_queue.remove(orders)
            elif order.type == OrderType.Hidden_Execution:
                # adjust the queue to reflect a hidden order execution
                pass
            else:
                # trading halt, what happens in the event of a trading halt
                pass

        return bid_order_queue, offer_order_queue

    def summary_statistics(self, time):
        bid_orders, offer_orders = self.__build(time)
        pass

    def animation(self):
        # produce an animation
        pass

    def volume_weighted_price(self, lower_limit, upper_limit):
        """
        :param lower_limit: lower time limit
        :param uppder_limit: upper time limit
        :return: Volume weighted average (traded) price
        """

        message_data = self.message_data[self.message_data['Time'] >= lower_limit]
        message_data = message_data[message_data['Time'] <= upper_limit]

        volume_weighted_price = 0.0

        # cumulative traded volume
        cumulative_volume = 0.0

        for message in message_data.index:
            if message_data['Type'][message] == OrderType.Visible_Execution.value or message_data['Type'][message] == OrderType.Hidden_Execution.value:
                volume_weighted_price += message_data['Price'][message] * message_data['Size'][message]
                cumulative_volume += message_data['Size'][message]

        return volume_weighted_price / cumulative_volume

    def order_summary(self, order_type, start_time, end_time):
        """
        :param order_type: submission, cancellation, deletion, execution
        :param start_time: start time
        :param end_time: end time
        :return: average price
        """
        import numpy as np

        message_data = self.message_data[self.message_data['Time'] >= start_time]
        message_data = message_data[message_data['Time'] <= end_time]
        message_data = message_data[message_data['Type'] == order_type.value]

        bid_orders_frame = message_data[message_data['Direction'] == 1]
        offer_orders_frame = message_data[message_data['Direction'] == -1]

        bid_orders_price = bid_orders_frame['Price']
        offer_orders_price = offer_orders_frame['Price']
        bid_orders_volume = bid_orders_frame['Size']
        offer_orders_volume = offer_orders_frame['Size']

        bid_mean_price = np.average(bid_orders_price)
        bid_std_price = np.std(bid_orders_price)
        bid_median_price = np.median(bid_orders_price)
        offer_mean_price = np.average(offer_orders_price)
        offer_std_price = np.std(offer_orders_price)
        offer_median_price = np.median(offer_orders_price)

        bid_mean_volume = np.average(bid_orders_volume)
        bid_std_volume = np.std(bid_orders_volume)
        bid_median_volume = np.median(bid_orders_volume)
        offer_mean_volume = np.average(offer_orders_volume)
        offer_std_volume = np.std(offer_orders_volume)
        offer_median_volume = np.median(offer_orders_volume)

        print('Start Time: {0}'.format(start_time))
        print('End Time: {0}'.format(end_time))
        print('Number of Events: {0}'.format(len(message_data.index)))
        print('Order Type: {0}'.format(order_type.name))
        print('---------------------------------------')
        print('{0} - {1}'.format('Bid Order', 'Ask Order'))
        print('Mean Price: {0:.2f} - {1:.2f}'.format(bid_mean_price, offer_mean_price))
        print('%10s' % 'Std: {0:.2f} - {1:.2f}'.format(bid_std_price, offer_std_price))
        print('Median Price: {0:.2f} - {1:.2f}'.format(bid_median_price, offer_median_price))
        print('Mean Volume: {0:.2f} - {1:.2f}'.format(bid_mean_volume, offer_mean_volume))
        print('%10s' % 'Std: {0:.2f} - {1:.2f}'.format(bid_std_volume, offer_std_volume))
        print('Median Volume: {0:.2f} - {1:.2f}'.format(bid_median_volume, offer_median_volume))
        print('---------------------------------------')

    def price_plot(self, start_time, end_time):
        """
        :param start_time: start time
        :param end_time: end time
        :return: plot price vs colume plots for bid and offers
        """
        import numpy as np
        import matplotlib.pyplot as plt

        message_data = self.message_data[self.message_data['Time'] >= start_time]
        message_data = message_data[message_data['Time'] <= end_time]

        bid_price = message_data[message_data['Direction'] == 1]
        bid_price = bid_price[bid_price['Type'] == OrderType.Submission.value]['Price'].unique()
        offer_price = message_data[message_data['Direction'] == -1]
        offer_price = offer_price[offer_price['Type'] == OrderType.Submission.value]['Price'].unique()

        bid_price = np.sort(bid_price)
        offer_price = np.sort(offer_price)

        bid_volume = np.zeros((len(bid_price), 1))
        offer_volume = np.zeros((len(offer_price), 1))
        cont = 0

        for price in bid_price:
            size = 0.0
            for idx in message_data.index:
                if message_data['Price'][idx] == price and message_data['Direction'][idx] == 1 and message_data['Type'][idx] == OrderType.Submission.value:
                    size += message_data['Size'][idx]
                if message_data['Price'][idx] == price and message_data['Direction'][idx] == 1 and (message_data['Type'][idx] == OrderType.Visible_Execution.value or message_data['Type'][idx] == OrderType.Hidden_Execution.value):
                    size -= message_data['Size'][idx]
            bid_volume[cont] = size
            cont += 1

        cont = 0

        for price in offer_price:
            size = 0.0
            for idx in message_data.index:
                if message_data['Price'][idx] == price and message_data['Direction'][idx] == -1:
                    size += message_data['Size'][idx]
                if message_data['Price'][idx] == price and message_data['Direction'][idx] == -1 and (message_data['Type'][idx] == OrderType.Visible_Execution.value or message_data['Type'][idx] == OrderType.Hidden_Execution.value):
                    size -= message_data['Size'][idx]
            offer_volume[cont] = size
            cont += 1

        plt.figure(1)

        plt.subplot(121)
        plt.bar(bid_price, bid_volume)

        plt.subplot(122)
        plt.bar(offer_price, offer_volume)

        plt.show()

if __name__ == '__main__':
    import datetime
    from Data.TimeSeriesRepository import TimeSeriesRepository
    from Enums.DataType import DataType
    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    ticker = 'AMZN'
    file_name = 'AMZN_2012-06-21_34200000_57600000_message_5.csv'
    start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
    end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
    date = datetime.datetime(year=2012, month=6, day=21)
    timeSeriesRepository = TimeSeriesRepository(file_path)
    msg_data = timeSeriesRepository.get_data(ticker, date, DataType.message, 5)
    lob = LimitOrderBook(msg_data)
    #vwap = lob.volume_weighted_price(0, 34300)
    #lob.order_summary(OrderType.Visible_Execution, 0, 34300)
    lob.price_plot(0, 34300)
    #print('VWAP: ' + str(vwap))
