
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.LimitOrderBook.OrderBookDataReader import OrderBookDataReader
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.SummaryStatistics import SummaryStatistics
from Analytics.LimitOrderBookPlot import LimitOrderBookPlot
from Analytics.StudentTDistribution import StudentTDistribution
from Analytics.LimitOrderBookSeries import LimitOrderBookSeries
from Analytics.StatisticalTests import StatisticalTests
from Analytics.LinearRegression import LinearRegression
from Analytics.LogisticRegression import LogisticRegression
from Analytics.GARCHModel import GARCHModel
from Analytics.HawkesProcess import HawkesProcess
from Analytics.PriceForecast import PriceForecast
from Analytics.EfficientPrice import EfficientPrice
from Analytics.ExtractPrices import ExtractPrices
from sklearn import svm
from Factory.TimeSeriesFactory import TimeSeriesFactory

from Enums.TimeSeriesTypes import TimeSeriesTypes


file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
order_file = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'


def reconstruct_order_book(file, data_type):
    """
    :param file: Data file
    :param data_type: Message data or Order data
    :return: A collection of books
    """
    limit_order_book = LimitOrderBook()

    if data_type == 'message':
        data_reader = MessageDataReader()
    elif data_type == 'order':
        data_reader = OrderBookDataReader()
    else:
        raise NotImplementedError('Data type not recognised')

    data_reader.read_data(file)
    lob_updater = LimitOrderBookUpdater(data_reader.messages)
    lob_updater.generate_order_book_series_from_message_data(limit_order_book)

    return lob_updater.books


def generate_time_series(time_series_type, limit_order_books, start_time, interval):
    """
    :param time_series_type: Type of time series
    :param limit_order_books: Collection of limit order books
    :param start_time: Time of first order book
    :param interval: Interval between books
    :return: Time series
    """
    time_series = TimeSeriesTypes(time_series_type)
    time_series_factory = TimeSeriesFactory(limit_order_books)
    output = time_series_factory.create_time_series(time_series, start_time, interval)
    return output


def calculate_summary_statistics(file, data_type):
    """
    :param file: Data file
    :param data_type: Data Type
    :return: Summary
    """

    if data_type == 'message':
        data_reader = MessageDataReader()
    else:
        raise NotImplementedError('Data type not recognised')

    data_reader.read_data(file)

    summary = SummaryStatistics(data_reader.messages)

    return summary.generate_summary()


def display_plot(file, data_type):
    """
    :param file: Data file
    :param data_type: Data Type
    :return: Summary
    """

    if data_type == 'message':
        data_reader = MessageDataReader()
    else:
        raise NotImplementedError('Data type not recognised')

    data_reader.read_data(file)

    summary = SummaryStatistics(data_reader.messages)

    plotter = LimitOrderBookPlot(summary, None)

    plotter.plot_submitted_volume()
    plotter.plot_deleted_volume()

    return None


def fit_statistical_distribution(time_series, distribution):
    """
    :param time_series: time series
    :param distribution: distribution
    :return:
    """

    if isinstance(time_series, LimitOrderBookSeries) is False:
        raise NotImplementedError('Time series type not recognised')

    if distribution == 'students-t':
        dist = StudentTDistribution()
    else:
        raise NotImplementedError('This distribution is not supported')

    return dist.fit_data(time_series)


def statistical_tests(time_series, test):
    """
    :param time_series: time series
    :param test: test
    :return:
    """

    if isinstance(time_series, LimitOrderBookSeries) is False:
        raise NotImplementedError('Time series type not recognised')

    stat_test = StatisticalTests()

    if test == 'chow':
        return stat_test.chow_test()
    elif test == 'hurst':
        return stat_test.hurst_exponent(time_series)
    else:
        raise NotImplementedError('Test not recognised')

    return None


def fit_linear_model(x, y, model_name):
    """
    :param time_series: time series
    :param model_name: model
    :return:
    """

    if model_name == 'linear':
        model = LinearRegression()
        return model.fit_data(x, y)
    elif model_name == 'logistic':
        model = LogisticRegression()
        return model.fit_data(x, y)
    else:
        raise NotImplementedError('Model not recognised')

    return None


def fit_non_linear_model(time_series, model):
    """
    :param time_series: time series
    :param model: model
    :return:
    """
    if isinstance(time_series, LimitOrderBookSeries) is False:
        return NotImplementedError('time series type not recognised')

    if model is not 'garch':
        raise NotImplementedError('Model not recognised')

    non_lin_model = GARCHModel()
    return non_lin_model.fit_data(time_series)


def hawkes_process_simulation(intensity, events, alpha, beta, l):
    """
    :param intensity: intensity rate
    :param events: number of events
    :param alpha: alpha
    :param beta: speed of mean reversion
    :param l: starting point
    :return: simulated time series
    """
    hawkes = HawkesProcess(intensity)
    time_series = hawkes.simulate_process(events,alpha, beta, l)
    return time_series


def mid_price_forecast(file):
    """
    :param file: data file
    :return:
    """
    # Using the SVM
    data_reader = OrderBookDataReader()
    data = data_reader.read_data(file)
    extract_prices = ExtractPrices()
    x, y = extract_prices.extract_data(data)
    clf = svm.SVC()
    clf.fit(x[0:990], y[0:990])
    output = []
    for i in range(991, 999):
        prediction = clf.predict(x[i])
        output.append(prediction[0])

    return output


def price_increase_probability(file, data_type):
    """
    :param file: file path
    :param data_type: data type
    :return: a function which can be used to calculate probabilites
    """
    books = reconstruct_order_book(file, data_type)
    time_series_factory = TimeSeriesFactory(books)
    price_forecast = PriceForecast(time_series_factory)
    prob, freq = price_forecast.calculate_size_deciles()
    outputs = price_forecast.calibrate_hidden_liquidity_parameter()
    return price_forecast.calculate_probability_up_move


def efficient_price(file, data_type, start_time, end_time):
    """
    :param file: data file
    :param data_type: data type
    :param start_time: start time
    :param end_time: end time
    :return: Time series of efficient price
    """
    # time series efficient price
    limit_order_book = LimitOrderBook()

    if data_type == 'message':
        data_reader = MessageDataReader()
    elif data_type == 'order':
        data_reader = OrderBookDataReader()
    else:
        raise NotImplementedError('Data type not recognised')

    data_reader.read_data(file)
    lob_updater = LimitOrderBookUpdater(data_reader.messages)
    lob_updater.generate_order_book_series_from_message_data(limit_order_book)

    time_series_factory = TimeSeriesFactory(lob_updater.books)
    bid, ask = time_series_factory.create_time_series(TimeSeriesTypes.price, start_time=start_time, time_interval=5)
    k = 150
    # what is this k
    eff_price = EfficientPrice(lob_updater)
    theta = eff_price.calculate_theta(k, start_time, end_time)
    price = eff_price.efficient_price(theta, bid)
    return price
