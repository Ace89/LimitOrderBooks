"""
    Aim:
        script of tests for functionality in the library

http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

"""

import pandas as pd
import sys
import numpy as np
import datetime
from numpy import exp
import matplotlib.pyplot as plt
from matplotlib import animation
from Enums.DataType import DataType
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Time.TimeStructure import TimeStructure
from Data.TimeSeriesRepository import TimeSeriesRepository
from sample.MessageData import MessageData
from sample.Utility import interpolate, auto_correlation, calib_garch, calib_arma, calib_auto_regressive
from sample.StatisticalDistributions import GumbelDist
from sample.StatisticalTests import linear_regression, sum_squared_errors, chow_test, hurst_exponent
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from scipy.stats import levy_stable
from statsmodels.tsa.api import VAR, DynamicVAR
from sample.OrderBookTimeSeries import OrderBookTimeSeries

ticker = 'AMZN'
file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5.csv'
start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
date = datetime.datetime(year=2012, month=6, day=21)

__all__ = ['test_create_time_buckets', 'ar_fit_test', 'data_bucket_structure_test',
           'string_bucket_test', 'message_data_test', 'auto_correl_test',
           'gumbel_dist', 'garch_test', 'chow_test', 'file_format', 'test_mle']


fig = plt.figure()
ax = plt.axes(xlim=(215,235), ylim=(0,80))
line, = ax.plot([], [], lw=2)


def test_create_time_buckets():
    """
    :return: average price, average volume and cumulative volume for buy and sell series
    """
    data_type = DataType.message
    time_series_repository = TimeSeriesRepository(file_path)
    time_structure = TimeStructure(start_date, end_date)
    time_structure.create_time_structure(300)
    order_type = OrderType.VisibleExecution
    order_direction = OrderDirection.Buy
    # populate the time_structure object with average values
    time_series_repository.create_time_bucket_structure(time_structure, ticker, date, data_type.name,
                                                        5, order_type, order_direction)
    avg_buckets = time_structure.time_structure

""" 
Have not created the order book trees yet
def test_order_book_trees():
    
    order book trees contain bid and offer levels instead of average prices
    
    data = pd.read_csv(file_path+file_name)
    levels = 3
    timeBuckets = TimeBuckets(data, 34200, 57600, 75)
    order_book_tree = timeBuckets. (levels)
    None
"""

def init():
    line.set_data([], [])
    return line,

"""
def test_limit_order_tree_buckets(i):
    
    data = pd.read_csv(file_path + file_name)
    nbins = 50
    timeBuckets = TimeBuckets(data, 34200, 57600, 75)
    # bucket_dict are actually arrays of 75 dictionaries
    [buy_bucket_dict, sell_bucket_dict] = timeBuckets.create_limit_order_tree_buckets(nbins)

    buy_bucket = buy_bucket_dict[i]
    sell_bucket = sell_bucket_dict[i]

    size = len(buy_bucket)

    x_buy = np.zeros((size))
    x_sell = np.zeros((size))
    y_buy = np.zeros((size))
    y_sell = np.zeros((size))

    j = 0
    for key in buy_bucket:
        x_buy[j] = key
        j+=1

    j = 0
    for key in sell_bucket:
        x_sell[j] = key
        j += 1

    x_buy.sort() # dictionary keys are not sorted values
    x_sell.sort()

    for j in range(0, len(x_buy)):
        y_buy[j] = buy_bucket[x_buy[j]]
        y_sell[j] = sell_bucket[x_sell[j]]
        x_buy[j] = x_buy[j] / 10000
        x_sell[j] = x_sell[j] / 10000

    #ax = plt.axes(xlim=(np.min(x_buy),np.max(x_buy)), ylim=(0,np.max(y_buy)))

    line.set_data([x_buy, x_sell], [y_buy, y_sell])
    return line,
"""

"""
def test_order_book_time_series():
    data = pd.read_csv(file_path+file_name)
    time_bucket = TimeBuckets(data, 34200, 57600, 75)
    order_book_time_series = OrderBookTimeSeries(time_bucket)

    avg_time_series = order_book_time_series.get_average_value_time_series('buy', 'price')
    avg_series_volume = order_book_time_series.get_average_value_time_series('buy', 'volume')
    order_time_series = order_book_time_series.get_order_book_time_series('buy', 'price', 3, 0)
    order_time_series_level1 = order_book_time_series.get_order_book_time_series('buy', 'price', 3, 1)
    order_time_series_level2 = order_book_time_series.get_order_book_time_series('buy', 'price', 3, 2)
    order_series_volume = order_book_time_series.get_order_book_time_series('buy', 'volume', 3, 0)
    order_series_level1 = order_book_time_series.get_order_book_time_series('buy', 'volume', 3, 1)
    order_series_level2 = order_book_time_series.get_order_book_time_series('buy', 'volume', 3, 2)
"""

def ar_fit_test():
    message_data = MessageData(file_path+file_name)
    message_data.read(10000)
    buys, sell_prices = message_data.get_buy_sell_prices()

    buy_prices = []

    for i in range(0,len(buys)):
        buy_prices.append(buys[i]/10000)

    train, test = buy_prices[1:len(buy_prices)-7], buy_prices[len(buy_prices)-7:]
    model = AR(train)
    model_fit = model.fit()
    window = model_fit.k_ar
    coef = model_fit.params
    history = train[len(train)-window:]
    history = [history[i] for i in range(len(history))]
    predictions = list()

    for t in range(len(test)):
        length = len(history)
        lag = [history[i] for i in range(length-window, length)]
        yhat = coef[0]
        for d in range(window):
            yhat += coef[d+1]*lag[window-d-1]
        obs = test[t]
        predictions.append(yhat)
        history.append(obs)
        print('predicted=%f, expected=%f' %(yhat, obs))

    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)

    plt.plot(test)
    plt.plot(predictions, color='red')
    plt.show()

    return None

"""
def data_bucket_structure_test():

    data = pd.read_csv(file_path + file_name)

    startTime = 34200  # 09:30 exchange open time
    endTime = 57600  # 16:00  exchange close time
    intervals = 75  # 75 intervals imply a 5 minute window

    dataBucket = TimeBuckets(data, startTime,endTime,intervals)
    sell_order = -1
    buy_order = 1
    [buy_buckets, buy_price, buy_size, buy_volume] = dataBucket.create_time_buckets(buy_order)

    [sell_buckets, sell_price, sell_size, sell_volume] = dataBucket.create_time_buckets(sell_order)

    # buckets will have one additional value
    plt.plot(buy_buckets[1:], buy_volume, 'b-', sell_buckets[1:], sell_volume, 'r--')
    plt.legend(['buy', 'sell'])
    plt.show()
    return None
"""

"""
def string_bucket_test():

    data = pd.read_csv(file_path + file_name)
    date = '1/1/2011'
    startTime = 34200  # 09:30 exchange open time
    # startTime = (34200/3600)
    endTime = 57600  # 16:00  exchange close time
    intervals = 75  # 75 intervals imply a 5 minute window
    levels = 3
    dataBucket = TimeBuckets(data,startTime,endTime,intervals)

    bid_prices = []
    bid_freq = []
    bid_vol1 = []
    bid_vol2 = []
    bid_vol3 = []
    ask_prices = []
    ask_freq = []
    ask_vol1 = []
    ask_vol2 = []
    ask_vol3 = []

    bucket_string = dataBucket.time_bucket(startTime, endTime, intervals, levels)

    for i in range(1, len(bucket_string)):
        ask_prices.append(bucket_string[i].best_ask_price/10000)
        ask_freq.append(bucket_string[i].ask_frequency)
        ask_vol1.append(bucket_string[i].ask_volume_levels["level0"])
        ask_vol2.append(bucket_string[i].ask_volume_levels["level1"])
        ask_vol3.append(bucket_string[i].ask_volume_levels["level2"])
        bid_prices.append(bucket_string[i].best_bid_price/10000)
        bid_freq.append(bucket_string[i].bid_frequency)
        bid_vol1.append(bucket_string[i].bid_volume_levels["level0"])
        bid_vol2.append(bucket_string[i].bid_volume_levels["level1"])
        bid_vol3.append(bucket_string[i].bid_volume_levels["level2"])

    # create a data frame containing the above series

    data_index = pd.date_range(date, periods=intervals, freq='5Min')

    data_dict = {'ask_price': pd.Series(ask_prices),
                 'bid_price': pd.Series(bid_prices),
                 'ask_vol1': pd.Series(ask_vol1),
                 'ask_vol2': pd.Series(ask_vol2),
                 'ask_vol3': pd.Series(ask_vol3),
                 'bid_vol1': pd.Series(bid_vol1),
                 'bid_vol2': pd.Series(bid_vol2),
                 'bid_vol3': pd.Series(bid_vol3),
                 'ask_freq': pd.Series(ask_freq),
                 'bid_freq': pd.Series(bid_freq)}

    data_frame = pd.DataFrame(data_dict)
    data_frame.index = data_index
    #data = np.log(data_frame).diff().dropna()

    model = VAR(data_frame)

    # need to create a data frame

    results = model.fit(1)
    print(results.summary())
    return None
"""

def message_data_test():
    ord_file = 'AMZN_2012-06-21_34200000_57600000_orderbook_5.csv'
    order_book = pd.read_csv(file_path + ord_file)
    order_book_data = order_book.as_matrix()
    x = np.arange(1, len(order_book_data) + 1)

    plt.plot(x, order_book_data[:, 1], '-b', x, order_book_data[:, 3], '--r')
    plt.legend(['Ask volume', 'Bid volume'])
    plt.show()

    message_data = MessageData(file_path + file_name)
    message_data.read(10000)
    message_data.short_summary()
    message_data.display()
    message_data.supply_demand()
    message_data.unpack_orders()
    print("Unique orders: " + str(len(message_data.orders)))
    print("Size of order dict: " + str(sys.getsizeof(message_data.orders)))

"""
def auto_correl_test():
    data = pd.read_csv(file_path + file_name)

    startTime = 34200  # 09:30 exchange open time
    endTime = 57600  # 16:00  exchange close time
    intervals = 75  # 75 intervals imply a 5 minute window

    dataBucket = TimeBuckets(data)
    sell_order = -1
    buy_order = 1
    [buy_buckets, buy_price, buy_size, buy_volume] = dataBucket.create_time_buckets(startTime,
                                                                                    endTime,
                                                                                    intervals,
                                                                                    buy_order)
    [sell_buckets, sell_price, sell_size, sell_volume] = dataBucket.create_time_buckets(startTime,
                                                                                        endTime,
                                                                                        intervals,
                                                                                        sell_order)
    # calculate the auto-correlation for the volumes
    lag = 1
    window_length = 10
    buy_auto_correl = auto_correlation(window_length, lag, buy_volume[1:])
    sell_auto_correl = auto_correlation(window_length,lag,sell_volume[1:])

    plt.plot(buy_auto_correl)
    plt.legend(['1day - buy correl'])
    plt.show()

    plt.plot(sell_auto_correl)
    plt.legend(['1day - sell correl'])
    plt.show()
"""

def gumbel_dist(execPrices):
    priceSeries = pd.Series(execPrices)
    dailyPriceDiffs = priceSeries.diff(periods=1)
    dailyPriceDiffs = dailyPriceDiffs[1:]
    dailyPctChange = priceSeries.pct_change()
    dailyPctChange = dailyPctChange[1:]

    bins = np.linspace(min(dailyPctChange), max(dailyPctChange), 100)
    hist, bins = np.histogram(dailyPctChange, bins)
    plt.plot(bins[:99], hist)

    # skew and kurt functions in pandas correct for bias, they do not in scipy

    average = dailyPctChange.mean()
    stdDev = dailyPctChange.std()
    skew = dailyPctChange.skew()
    kurt = dailyPctChange.kurt()

    # aperi = 1.2020569 not sure what this is for

    gumbel = GumbelDist(average, stdDev)
    sorted_returns = []

    for i in range(1, len(dailyPctChange) + 1):
        sorted_returns.append(dailyPctChange[i])

    fitted_pdf = gumbel.fit_pdf(sorted_returns)

    plt.plot(sorted_returns, fitted_pdf)
    plt.show()
    return None

"""
def garch_test():
    data = pd.read_csv(file_path + file_name)

    startTime = 34200  # 09:30 exchange open time
    endTime = 57600  # 16:00  exchange close time
    intervals = 75  # 75 intervals imply a 5 minute window

    dataBucket = TimeBuckets(data)
    sell_order = -1
    buy_order = 1
    [buy_buckets, buy_price, buy_size, buy_volume] = dataBucket.create_time_buckets(startTime,
                                                                                    endTime,
                                                                                    intervals,
                                                                                    buy_order)
    [sell_buckets, sell_price, sell_size, sell_volume] = dataBucket.create_time_buckets(startTime,
                                                                                        endTime,
                                                                                        intervals,
                                                                                        sell_order)

    volume = buy_volume[1:]
    data = np.zeros((len(volume) - 1, 1))

    for i in range(1, len(data)):
        data[i - 1] = np.log(volume[i] / volume[i - 1])

    estimates = calib_garch(data)

    for val in estimates:
        print(str(val))
    return None
"""

def chow_test():
    n_sims = 100
    x = np.zeros((n_sims, 1))
    y = np.zeros((n_sims, 1))

    for i in range(0, n_sims):
        x[i] = np.random.randn()
        y[i] = np.random.randn()

    # compare this value with an F test
    t_stat = chow_test(x, y, 20, 20)

    print("chow test val: " + str(t_stat))
    return None


def file_format():
    """
    Format of Message file
    Columns:
            1)  Time:
                Seconds after midnight with decimal
                precision of at least milliseconds
                and up to nanoseconds depending on
                the requested period
            2)  Type:
                1: Submission of a new limit order
                2: Cancellation (Partial deletion
                   of a limit order)
                3: Deletion (Total deletion of a limit order)
                4: Execution of a visible limit order
                5: Execution of a hidden limit order
                7: Trading halt indicator
                   (Detailed information below)
            3)  Order ID:
                Unique order reference number
                (Assigned in order flow)
            4)  Size:
                Number of shares
            5)  Price:
                Dollar price times 10000
                (i.e., A stock price of $91.14 is given
                by 911400)
            6)  Direction:
                -1: Sell limit order
                1: Buy limit order

                Note:
                Execution of a sell (buy) limit
                order corresponds to a buyer (seller)
                initiated trade, i.e. Buy (Sell) trade.

    As the data is read in from the CSV file, it has no column names

    """
    return None


def test_mle():

    # fit an AR(1) model to bucket data, then produce one-day forecasts
    # assume data follows a normal distribution
    # use Maximum likelihood estimation to fit mu and std deviation
    # for forecast produce upper bound and lower bound using 95th and 5th percentiles from Gaussian dist

    pass

if __name__ == '__main__':
    #test_limit_order_tree_buckets()
    #test_order_book_trees()
    #test_create_time_buckets()
    #test_order_book_time_series()
    #anim = animation.FuncAnimation(fig, test_limit_order_tree_buckets, init_func=init, frames=75,
    #                               interval=75, blit=True)
    #plt.show()
    test_create_time_buckets()


