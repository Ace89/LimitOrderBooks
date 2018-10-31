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
from Analytics.StudentTDistribution import StudentTDistribution
from Analytics.LimitOrderBookPlot import LimitOrderBookPlot
from Analytics.IStatisticalTest import IStatisticalTest
from Analytics.LinearRegression import LinearRegression
from Analytics.GARCHModel import GARCHModel
from Analytics.HawkesProcess import HawkesProcess
from Enums.OrderType import OrderType
from Enums.TimeSeriesTypes import TimeSeriesTypes

import Api

file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
order_file = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'


def test_api_orderbook_reconstruction():
    # data type: 'order_data', 'message'
    output = Api.reconstruct_order_book(file_path+order_file, file_path+file_name, 'message')
    pass


def test_order_book_update():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_empty_order_book(lob)
    lob_updater.generate_books_from_message_data(lob)
    books = lob_updater.books[-1]
    levels=5
    bid_queue = lob.get_bid_price_size(levels)
    ask_queue = lob.get_ask_price_size(levels)

    print('Bid Orders')
    for bid in bid_queue:
        print('price: {0}, size: {1}'.format(bid[0], bid[1]))

    print('Ask Orders')
    for ask in ask_queue:
        print('price: {0}, size: {1}'.format(ask[0], ask[1]))

    None


def order_book_update_series_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_empty_order_book(lob)
    order_book_series = lob_updater.generate_books_from_message_data(lob)
    time_series_factory = TimeSeriesFactory(lob_updater.books)
    bid_price, ask_price = time_series_factory.create_time_series_from_order_book_series(order_book_series,
                                                                                         TimeSeriesTypes.price,
                                                                                         start_time, time_interval)
    plt.plot(bid_price, color='b')
    plt.plot(ask_price, color='r')
    plt.legend(['Bid', 'Ask'])
    plt.show()


def order_book_updated_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_empty_order_book(lob)
    order_book_series = lob_updater.generate_books_from_message_data(lob)
    # books = lob_updater.update_order_book()
    # time_series_factory = TimeSeriesFactory(books)
    time_series_factory = TimeSeriesFactory(lob_updater.books)

    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price,
                                                                  start_time,
                                                                  time_interval)

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)
    imbalance_output = time_series_factory.create_time_series(TimeSeriesTypes.imbalance, start_time=34200, time_interval=5)

    print('number of limit orders: {0}'.format(num_limit_orders))

    bid = np.asarray(bid_price.tolist())
    ask = np.asarray(ask_price.tolist())
    imbalance = np.asarray(imbalance_output)
    plt.subplot(3, 1, 1)
    plt.plot(bid/10000)
    plt.title('Bid')

    plt.subplot(3, 1, 2)
    plt.plot(ask/10000)
    plt.title('Ask')

    plt.subplot(3, 1, 3)
    plt.plot(imbalance/10000)
    plt.title('Imbalance')

    plt.show()


def order_book_data_example():
    lob = LimitOrderBook()
    msg_data_reader = OrderBookDataReader(file_path+file_name)

    start_time = 34200
    time_interval = 5

    lob_updater = LimitOrderBookUpdater(None)
    order_data = msg_data_reader.read_data(file_path+order_file)
    lob_updater.add_order_book_data(order_data)
    lob_updater.generate_books_from_order_book_data(lob)
    print(len(lob_updater.books))


def create_time_series_example():
    #lob = LimitOrderBook()
    #msg_data_reader = MessageDataReader()
    order_data_reader = OrderBookDataReader()
    order_data_reader.read_data(file_path + order_file,file_path + file_name)
    #msg_data_reader.read_data(file_path + file_name)
    #lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    #lob_updater.update_empty_order_book(lob)
    #lob_updater.update_order_book(lob)

    time_series_factory = TimeSeriesFactory(None)
    bid, ask = time_series_factory.create_time_series_order_book(order_data_reader.messages,
                                                      TimeSeriesTypes.price,
                                                      start_time=34200,
                                                      time_interval=1)

    full_size_bid, full_size_ask = time_series_factory.create_time_series_order_book(order_data_reader.messages,
                                                                 TimeSeriesTypes.full_size,
                                                                 start_time=34200,
                                                                 time_interval=5)

    mid_price = time_series_factory.create_time_series_order_book(order_data_reader.messages,
                                                                  TimeSeriesTypes.mid_price,
                                                                  start_time=34200,
                                                                  time_interval=5)

    imbalance = time_series_factory.create_time_series_order_book(order_data_reader.messages,
                                                                  TimeSeriesTypes.imbalance,
                                                                  start_time=34200,
                                                                  time_interval=5)

    bid_rets = bid.pct_change().tolist()

    bid_rets = bid_rets[1:]

    bins = np.linspace(np.min(bid_rets), np.max(bid_rets), 100)

    plt.hist(bid_rets, bins)
    plt.show()

    plt.subplot(2, 1, 1)
    plt.plot(bid.tolist())
    plt.title('Bid')

    plt.subplot(2,1,2)
    plt.plot(ask.tolist())
    plt.title('Ask')

    plt.show()
    """
    plt.subplot(4,1,1)
    plt.plot(full_size_bid.tolist())
    plt.title('Full Size Bid')

    plt.subplot(4, 1, 2)
    plt.plot(full_size_ask.tolist())
    plt.title('Full Size Ask')
    """
    plt.subplot(2, 1, 1)
    plt.plot(mid_price.tolist())
    plt.title('Mid Price')

    plt.subplot(2, 1, 2)
    plt.plot(imbalance.tolist())
    plt.title('Imbalance')

    plt.show()


def limit_order_frequency_example():

    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    start = time.time()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.generate_books_from_message_data(lob)

    num_limit_orders = lob_updater.number_of_limit_order(OrderType.Submission, 34200, 57600)

    print('number of limit orders: {0}'.format(num_limit_orders))

    end = time.time()


def limit_order_efficient_price_example():
    from Analytics.EfficientPrice import EfficientPrice
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.generate_books_from_message_data(lob)

    efficient_price = EfficientPrice(lob_updater)

    theta = efficient_price.calculate_theta()
    print('Sum of theta {0}'.format(np.sum(theta)))

    time_series_factory = TimeSeriesFactory(lob_updater.books)
    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price, 34200, 1)

    bid_price = bid_price.tolist()

    eff_price, spread = efficient_price.calculate_efficient_price(theta, bid_price)

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


def visualize_example():
    msg_data_reader = MessageDataReader()
    order_data_reader = OrderBookDataReader()
    order_data_reader.read_data(file_path + order_file, file_path + file_name)
    msg_data_reader.read_data(file_path + file_name)
    summary_stats = SummaryStatistics(msg_data_reader.messages)

    lob_plot = LimitOrderBookPlot(summary_stats, order_data_reader.messages)
    #lob_plot.plot_event_price_volume()
    lob_plot.plot_vwap()
    #lob_plot.plot_submitted_volume()
    #lob_plot.plot_deleted_volume()

    #time_series_factory = TimeSeriesFactory(None)
    #bid, ask = time_series_factory.create_time_series_order_book(order_data,
     #                                                            TimeSeriesTypes.size,
      #                                                           start_time=34200,
       #                                                          time_interval=5)
    #lob_plot.plot_price_size(bid)


def fit_distribution_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.generate_books_from_message_data(lob)

    time_series_factory = TimeSeriesFactory(lob_updater.books)

    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price,
                                                                  start_time,
                                                                  time_interval)

    student_distribution = StudentTDistribution()
    fitted_parameters = student_distribution.fit_data(bid_price.tolist())


def statistical_test_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5
    lags =5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.generate_books_from_message_data(lob)

    time_series_factory = TimeSeriesFactory(lob_updater.books)

    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price,
                                                                  start_time,
                                                                  time_interval)

    statistical_tests = IStatisticalTest()
    test_value = statistical_tests.hurst_exponent(bid_price.tolist(), lags)


def linear_model_example():
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()
    start_time = 34200
    time_interval = 5
    lags = 5

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.generate_books_from_message_data(lob)

    time_series_factory = TimeSeriesFactory(lob_updater.books)

    bid_price, ask_price = time_series_factory.create_time_series(TimeSeriesTypes.price,
                                                                  start_time,
                                                                  time_interval)

    linear_regression = LinearRegression()
    fitted_parameters = linear_regression.fit_data(bid_price.tolist(), ask_price.tolist())


def hawkes_process_example():
    intensity_rate = 1.2
    num_events = 100
    alpha = 0.6
    beta = 0.8

    hawkes = HawkesProcess(intensity_rate)
    events = hawkes.generate_events(num_events)
    event_times, intensity_rates = hawkes.simulate_process(events, alpha, beta, intensity_rate)


def gaussian_distribution_fitting():
    samples=1000
    steps=100
    mu=0.0
    sigma = 1.0
    rnd = np.random.normal(loc=mu, scale=sigma, size=samples)

    #bins = np.linspace(np.min(rnd), np.max(rnd), steps)

    count, bins, ignored = plt.hist(rnd, bins=steps)
    plt.show()
    count = np.append([0],count)
    plt.bar(bins, count/steps, width=0.1,color='b')
    plt.plot(bins,
             1/(sigma * np.sqrt(2 * np.pi))*np.exp(-(bins - mu)**2/(2*sigma**2)),
             linewidth=2, color='r')
    plt.title('Gaussian distribution fitting')
    plt.legend(['Fitted Values', 'Data'])
    plt.show()
    return None


def student_distribution_fitting():
    from scipy.stats import t
    samples = 1000
    steps = 100
    df = 5

    rnd = np.random.standard_t(df, samples)

    count, bins, ignored = plt.hist(rnd, bins=steps)
    plt.show()
    count = np.append([0], count)
    plt.bar(bins, count / steps, width=0.1, color='b')
    rv=t(df)
    plt.plot(bins,
             rv.pdf(bins),
             linewidth=2, color='r')
    plt.title('Student t distribution fitting')
    plt.legend(['Fitted Values', 'Data'])
    plt.show()

    return None

if __name__ == '__main__':
    #test_order_book_update()
    #order_book_updated_example()
    #order_book_update_series_example()
    #create_time_series_example()
    #limit_order_frequency_example()
    #limit_order_efficient_price_example()
    #svm_example()
    #summary_statistics()
    #visualize_example()
    #order_book_data_example()
    #gaussian_distribution_fitting()
    #student_distribution_fitting()
    test_api_orderbook_reconstruction()