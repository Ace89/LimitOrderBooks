
from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater
from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
from Factory.TimeSeriesFactory import TimeSeriesFactory
from Enums.TimeSeriesTypes import TimeSeriesTypes

import numpy as np


file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'


class PriceForecast:

    def __init__(self, time_series_factory):
        self.time_series_factory = time_series_factory
        self.prob_dict = {}
        self.freq_dict = {}
        self.liquidity_parameter = None

    def calculate_size_deciles(self):
        bid_size, ask_size = self.time_series_factory.create_time_series(TimeSeriesTypes.full_size, 34201, 1)
        mid_price = self.time_series_factory.create_time_series(TimeSeriesTypes.mid_price,34201,1)
        deciles = np.arange(0, 100, 10)
        bid_deciles = np.percentile(bid_size, deciles)
        ask_deciles = np.percentile(ask_size, deciles)

        sizes = list(zip(bid_size, ask_size))
        sizes_price = list(zip(sizes, mid_price))

        # calculate mid price move

        sizes_price_change = list()
        for i in range(1, len(sizes_price)):
            if sizes_price[i][1] - sizes_price[i-1][1] > 0:
                sizes_price_change.append(1)
            else:
                sizes_price_change.append(0)

        # this is for padding as when I calc absolute price moves, I lose the first value
        sizes_price_change = [0] + sizes_price_change

        sizes_price_change = list(zip(sizes, sizes_price_change))

        count = []

        unique_bid_values = np.unique(bid_deciles)
        unique_ask_values = np.unique(ask_deciles)

        val = unique_bid_values[0]
        ask = unique_ask_values[0]
        cont = list(filter(lambda x: x[0] <= val, sizes))
        cont = list(filter(lambda x: x[1] <= ask, cont))
        count.append(((val, ask), len(cont)))

        for i in range(1, len(unique_ask_values)):
            val = unique_bid_values[0]
            cont = list(filter(lambda x: x[0] <= val, sizes))
            cont = list(filter(lambda x: unique_ask_values[i-1] <= x[1] < unique_ask_values[i], cont))
            count.append(((val, unique_ask_values[i]), len(cont)))

        for i in range(1, len(unique_bid_values)):
            ask = unique_ask_values[0]
            cont = list(filter(lambda x: unique_bid_values[i-1] <= x[0] < unique_bid_values[i], sizes))
            cont = list(filter(lambda x: x[1] <= ask, cont))
            count.append(((unique_bid_values[i], ask), len(cont)))

        for i in range(1, len(unique_bid_values)):
            for j in range(1, len(unique_ask_values)):
                cont = list(filter(lambda x: unique_bid_values[i-1] <= x[0] < unique_bid_values[i], sizes))
                cont = list(filter(lambda x: unique_ask_values[j-1] <= x[1] < unique_ask_values[j], cont))
                count.append(((unique_bid_values[i], unique_ask_values[j]), len(cont)))

        sum_count = []

        total_up_moves = 0

        for changes in sizes_price_change:
            total_up_moves += changes[1]

        val = unique_bid_values[0]
        cont = list(filter(lambda x: x[0][0] <= val, sizes_price_change))
        cont = list(filter(lambda x: x[0][1] <= unique_ask_values[0], cont))
        cont = [temp[1] for temp in cont]
        sum_count.append(((val, ask), sum(cont)/total_up_moves))

        for i in range(1, len(unique_ask_values)):
            val = unique_bid_values[0]
            cont = list(filter(lambda x: x[0][0] <= val, sizes_price_change))
            cont = list(filter(lambda x: unique_ask_values[i - 1] <= x[0][1] < unique_ask_values[i], cont))
            cont = [temp[1] for temp in cont]
            sum_count.append(((val, unique_ask_values[i]), sum(cont)/total_up_moves))

        for i in range(1, len(unique_bid_values)):
            cont = list(filter(lambda x: unique_bid_values[i - 1] <= x[0][0] < unique_bid_values[i], sizes_price_change))
            cont = list(filter(lambda x: x[0][1] <= unique_ask_values[0], cont))
            cont = [temp[1] for temp in cont]
            sum_count.append(((unique_bid_values[i], unique_ask_values[0]), sum(cont)/total_up_moves))

        for i in range(1, len(unique_bid_values)):
            for j in range(1, len(unique_ask_values)):
                cont = list(filter(lambda x: unique_bid_values[i - 1] <= x[0][0] < unique_bid_values[i], sizes_price_change))
                cont = list(filter(lambda x: unique_ask_values[j - 1] <= x[0][1] < unique_ask_values[j], cont))
                cont = [temp[1] for temp in cont]
                sum_count.append(((unique_bid_values[i], unique_ask_values[j]), sum(cont)/total_up_moves))

        for val in sum_count:
            self.prob_dict[val[0]] = val[1]

        for val in count:
            self.freq_dict[val[0]] = val[1]

        return self.prob_dict, self.freq_dict

    def least_squares_error_function(self, h):
        """
        :param h: liquidity parameter
        :return: least squares sum for a given h
        """
        squared_sum = 0

        for key in list(self.freq_dict):
            theoretical_prob = (key[0]+h) /(key[0]+key[1]+2*h)
            diff = (self.prob_dict[key] - theoretical_prob)**2
            squared_sum = diff*self.freq_dict[key]

        return squared_sum

    def calibrate_hidden_liquidity_parameter(self):
        from scipy.optimize import least_squares
        h = 0.15
        res = least_squares(self.least_squares_error_function, h)
        self.liquidity_parameter = res.x[0]
        return [res.x, res.cost, res.optimality]

    def calculate_probability_up_move(self, bid_size, ask_size):
        # bid size and ask size have to be percentiles as in 0.1..0.9 and not volumes
        # deciles correspond to volume sizes
        prob = (bid_size + self.liquidity_parameter) / (bid_size+ask_size + 2*self.liquidity_parameter)
        return prob

    def calculate_empirical_probability(self):
        pass

    def least_squares_to_minimize(self):
        pass

if __name__ == '__main__':
    lob = LimitOrderBook()
    msg_data_reader = MessageDataReader()

    msg_data_reader.read_data(file_path + file_name)
    lob_updater = LimitOrderBookUpdater(msg_data_reader.messages)
    lob_updater.update_order_book(lob)
    time_series_factory = TimeSeriesFactory(lob_updater.books)
    price_forecast = PriceForecast(time_series_factory)

    h = 0.15
    prob, freq = price_forecast.calculate_size_deciles()
    sq_sum = price_forecast.least_squares_error_function(h)
    params = price_forecast.calibrate_hidden_liquidity_parameter()
    print('Least squares {0}'.format(sq_sum))
    print('Calibrated value {0}'.format(params[0]))
    print('Cost value {0}'.format(params[1]))
    print('Optimality value {0}'.format(params[2]))

