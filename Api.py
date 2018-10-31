
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Analytics.SummaryStatistics import SummaryStatistics
from Analytics.LimitOrderBookPlot import LimitOrderBookPlot


from api.ReconstructOrderBookHandler import ReconstructOrderBookHandler
from api.GenerateTimeSeriesHandler import GenerateTimeSeriesRequestHandler
from api.SummaryStatisticsHandler import SummaryStatisticsHandler
from api.FitDistributionHandler import FitDistributionHandler
from api.StatisticalTestsHandler import StatisticalTestsHandler
from api.FitLinearModelHandler import FitLinearModelHandler
from api.FitNonLinearModel import FitNonLinearModel
from api.ProcessSimulationHandler import HawkesProcessSimulation
from api.PriceForecastHandler import PriceForecastHandler
from api.PriceProbabilityHandler import PriceProbabilityHandler
from api.EfficientPriceHandler import EfficientPriceHandler

file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'
order_file = 'AMZN_2012-06-21_34200000_57600000_orderbook_5_subset.csv'


def reconstruct_order_book(order_file, message_data_file, data_type):
    """
    :param file: Data file
    :param data_type: Message data or Order data
    :return: A collection of books
    """
    order_book_handler = ReconstructOrderBookHandler()
    order_book_series = order_book_handler.handle_request(order_file, message_data_file, data_type)

    return order_book_series


def generate_time_series(time_series_type, limit_order_books, start_time, interval):
    """
    :param time_series_type: Type of time series
    :param limit_order_books: Collection of limit order books
    :param start_time: Time of first order book
    :param interval: Interval between books
    :return: Time series
    """
    time_series_handler = GenerateTimeSeriesRequestHandler()
    output = time_series_handler.handle_request(time_series_type, limit_order_books, start_time, interval)
    return output


def calculate_summary_statistics(file, data_type):
    """
    :param file: Data file
    :param data_type: Data Type
    :return: Summary
    """

    summary_stats_handler = SummaryStatisticsHandler()
    summary = summary_stats_handler.handle_request(file, data_type)

    return summary


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
    handler = FitDistributionHandler()
    fitted_params = handler.handle_request(time_series, distribution)
    return fitted_params


def statistical_tests(time_series, test):
    """
    :param time_series: time series
    :param test: test
    :return:
    """

    handler = StatisticalTestsHandler()
    stat_test = handler.handle_request(time_series, test)
    return stat_test


def fit_linear_model(x, y, model_name):
    """
    :param time_series: time series
    :param model_name: model
    :return:
    """

    handler = FitLinearModelHandler()
    output = handler.handle_request(model_name, x, y)
    return output


def fit_non_linear_model(time_series, model):
    """
    :param time_series: time series
    :param model: model
    :return:
    """
    handle = FitNonLinearModel()
    output = handle.handle_request(model, time_series)
    return output


def hawkes_process_simulation(intensity, events, alpha, beta, l):
    """
    :param intensity: intensity rate
    :param events: number of events
    :param alpha: alpha
    :param beta: speed of mean reversion
    :param l: starting point
    :return: simulated time series
    """
    hawkes = HawkesProcessSimulation()
    time_series = hawkes.handle_request(intensity, events,alpha, beta, l)
    return time_series


def mid_price_forecast(file):
    """
    :param file: data file
    :return:
    """

    handle = PriceForecastHandler()
    output = handle.handle_request(file)
    return output


def price_increase_probability(file, data_type):
    """
    :param file: file path
    :param data_type: data type
    :return: a function which can be used to calculate probabilites
    """
    handler = PriceProbabilityHandler()
    output = handler.handle_Request(file, data_type)
    return output


def efficient_price(file, data_type, start_time, end_time):
    """
    :param file: data file
    :param data_type: data type
    :param start_time: start time
    :param end_time: end time
    :return: Time series of efficient price
    """
    # time series efficient price
    handler = EfficientPriceHandler()
    output = handler.handle_request(file, data_type, start_time, end_time)
    return output
