import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.ExtractPrices import ExtractPrices
from Analytics.SummaryStatistics import SummaryStatistics
from Factory.TimeSeriesFactory import TimeSeriesFactory
from Enums.OrderType import OrderType
from Enums.TimeSeriesTypes import TimeSeriesTypes

file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'


def order_book_updated_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_order_book(lob)

    time_series_factory = TimeSeriesFactory(lob_updater.books)

    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price,
                                                                  start_time,
                                                                  time_interval)

    #bid_price, ask_price = lob_updater.create_time_series()

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)

    imbalance_output = lob_updater.create_time_series(start_time=34200, time_interval=5, series_type=TimeSeriesTypes.imbalance)

    print('number of limit orders: {0}'.format(num_limit_orders))

    bid = np.asarray(bid_price.tolist())
    ask = np.asarray(ask_price.tolist())

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


def order_book_imbalance_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    start = time.time()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_order_book(lob)

    imbalance_output = lob_updater.create_time_series(start_time=34200, time_interval=5, series_type='imbalance')

    plt.plot(imbalance_output)
    plt.title('Imbalance')

    plt.show()

    end = time.time()


def limit_order_frequency_example():

    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    start = time.time()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_order_book(lob)

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)

    print('number of limit orders: {0}'.format(num_limit_orders))

    end = time.time()


def limit_order_efficient_price_example():

    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_order_book(lob)

    theta = lob_updater.calculate_efficient_price()
    print('Sum of theta {0}'.format(np.sum(theta)))
    spread = list()
    for i in range(1, 140):
        cont = list(filter(lambda x: x <= i, theta))
        spread.append(np.sum(cont) / 150)

    bid_price, ask_price = lob_updater.create_time_series(start_time=34200, time_interval=1,series_type='price')

    eff_price = list()

    for i in range(0,len(bid_price)):
        eff_price.append(bid_price[i]+spread[0])

    plt.subplot(3, 1, 1)
    plt.plot(theta)
    plt.title('Theta')

    plt.subplot(3, 1, 2)
    plt.plot(spread)
    plt.title('Spread')

    plt.subplot(3, 1, 3)
    plt.plot(eff_price)
    plt.title('Efficient Price')

    plt.show()


def svm_example():
    order_file_name = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'
    data_reader = OrderBookDataReader()
    data = data_reader.read_data(file_path + order_file_name)
    extract_prices = ExtractPrices()
    x, y = extract_prices.extract_data(data)
    clf = svm.SVC()
    clf.fit(x[0:990], y[0:990])

    for i in range(991, 999):
        prediction = clf.predict(x[i])
        print('{0} : {1}'.format(prediction[0], y[i]))


def summary_statistics():
    msg_data_reader = MessageDataReader()
    msg_data_reader.read_data(file_path + file_name)
    summary_stats = SummaryStatistics(msg_data_reader.messages)
    summary_stats_result = summary_stats.generate_summary()
    print('results created')


if __name__ == '__main__':
    order_book_updated_example()
    #limit_order_frequency_example()
    #limit_order_efficient_price_example()
    #svm_example()
    #summary_statistics()