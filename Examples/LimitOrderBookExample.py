import time
import matplotlib.pyplot as plt
import numpy as np

from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Enums.OrderType import OrderType

file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'


def order_book_updated_example():
    lob = LimitOrderBook()
    msgDataReader = MessageDataReader()

    start = time.time()

    msgDataReader.read_messages(file_path+file_name)
    lob_updater = LimitOrderBookUpdater(msgDataReader.messages)
    lob_updater.update_order_book(lob)

    bid_price, ask_price = lob_updater.create_time_series()

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)

    imbalance_output = lob_updater.create_time_series(start_time=34200, time_interval=5, series_type='imbalance')

    print('number of limit orders: {0}'.format(num_limit_orders))

    bid = np.asarray(bid_price)
    ask = np.asarray(ask_price)

    plt.subplot(3, 1, 1)
    plt.plot(bid/10000)
    plt.title('Bid')

    plt.subplot(3, 1, 2)
    plt.plot(ask/10000)
    plt.title('Ask')

    plt.subplot(3, 1, 3)
    plt.plot(imbalance_output)
    plt.title('Imbalance')

    plt.show()

    end = time.time()


def order_book_imbalance_example():
    lob = LimitOrderBook()
    msgDataReader = MessageDataReader()

    start = time.time()

    msgDataReader.read_messages(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msgDataReader.messages)
    lob_updater.update_order_book(lob)

    imbalance_output = lob_updater.create_time_series(start_time=34200, time_interval=5, series_type='imbalance')

    plt.plot(imbalance_output)
    plt.title('Imbalance')

    plt.show()

    end = time.time()


def limit_order_frequency_example():

    lob = LimitOrderBook()
    msgDataReader = MessageDataReader()

    start = time.time()

    msgDataReader.read_messages(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msgDataReader.messages)
    lob_updater.update_order_book(lob)

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)

    print('number of limit orders: {0}'.format(num_limit_orders))

    end = time.time()


if __name__ == '__main__':
    order_book_updated_example()
