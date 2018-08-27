
from Analytics.Features import Features


class ExtractPrices(Features):

    def __init__(self):
        pass

    def extract_data(self, data):
        """
        :param data: data frame
        :return: time series
        """
        levels = len(data.columns) / 4
        ask_price = data['AskPrice1'].tolist()
        ask_size = data['AskSize1'].tolist()
        bid_price = data['BidPrice1'].tolist()
        bid_size = data['BidSize1'].tolist()
        mid_price = [0.5*(ask_price[i]+bid_price[i]) for i in range(0,len(ask_price))]
        input_data = list()
        output_data = list()
        for i in range(0, len(ask_price)):
            feature_set = list()
            feature_set.append(ask_price[i])
            feature_set.append(ask_size[i])
            feature_set.append(bid_price[i])
            feature_set.append(bid_size[i])
            input_data.append(feature_set)

        for i in range(1, len(mid_price)):
            delta = mid_price[i] - mid_price[i-1]

            if delta > 0:
                output_data.append('Upward')
            elif delta < 0:
                output_data.append('Downward')
            else:
                output_data.append('Stationary')

        return [input_data[:-1], output_data]
