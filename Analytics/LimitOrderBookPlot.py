
import matplotlib.pyplot as plt
import numpy as np
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection


class LimitOrderBookPlot:

    def __init__(self, summary_stats, order_data):
        self.summary_stats = summary_stats
        self.order_data = order_data

    def plot_submitted_volume(self):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        buy_size = self.summary_stats.size_order_buy_sell()
        sell_size = self.summary_stats.size_order_buy_sell(OrderType.Submission, OrderDirection.Sell)

        fig, ax = plt.subplots()
        idx = np.arange(1, 3)

        ax.set_ylabel('Size')

        pb, ps = plt.bar(idx, (np.sum(buy_size), np.sum(sell_size)))
        pb.set_facecolor('r')
        ps.set_facecolor('b')
        ax.set_xticks(idx)
        ax.set_xticklabels(['Buy', 'Sell'])
        ax.set_ylabel('Size')
        ax.set_title('Buy and Sell Order Sizes')
        plt.show()

    def plot_deleted_volume(self):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        buy_size = self.summary_stats.size_order_buy_sell(OrderType.Deletion, OrderDirection.Buy)
        sell_size = self.summary_stats.size_order_buy_sell(OrderType.Deletion, OrderDirection.Sell)

        fig, ax = plt.subplots()
        idx = np.arange(1, 3)

        pb, ps = plt.bar(idx, [np.sum(buy_size), np.sum(sell_size)])
        pb.set_facecolor('r')
        ps.set_facecolor('b')
        ax.set_xticks(idx)
        ax.set_xticklabels(['Buy', 'Sell'])
        ax.set_ylabel('Size')
        ax.set_title('Buy and Sell Deleted Sizes')
        plt.show()

    def plot_price_size(self, limit_order_book_series):
        fig, ax = plt.subplots()
        plt.plot(limit_order_book_series.index, limit_order_book_series.tolist())
        ax.set_ylabel('Price $')
        ax.set_title('Bid price')
        plt.show()

    def plot_event_price_volume(self):
        best_ask = self.order_data['AskPrice1'].tolist()
        best_bid = self.order_data['BidPrice1'].tolist()
        events = np.arange(0, len(best_ask))

        data = self.order_data

        scale = 10000

        bid_prices = [data['BidPrice1'].tolist()[-1]/scale,
                      data['BidPrice2'].tolist()[-1]/scale,
                      data['BidPrice3'].tolist()[-1]/scale,
                      data['BidPrice4'].tolist()[-1]/scale,
                      data['BidPrice5'].tolist()[-1]/scale]

        bid_volumes = [data['BidSize1'].tolist()[-1],
                      data['BidSize2'].tolist()[-1],
                      data['BidSize3'].tolist()[-1],
                      data['BidSize4'].tolist()[-1],
                      data['BidSize5'].tolist()[-1]]

        ask_prices = [data['AskPrice1'].tolist()[-1]/scale,
                      data['AskPrice2'].tolist()[-1]/scale,
                      data['AskPrice3'].tolist()[-1]/scale,
                      data['AskPrice4'].tolist()[-1]/scale,
                      data['AskPrice5'].tolist()[-1]/scale]

        ask_volumes = [data['AskSize1'].tolist()[-1],
                       data['AskSize2'].tolist()[-1],
                       data['AskSize3'].tolist()[-1],
                       data['AskSize4'].tolist()[-1],
                       data['AskSize5'].tolist()[-1]]

        plt.figure()
        plt.subplot(122)
        plt.plot(events, best_ask, color='r')
        plt.plot(events, best_bid, color='b')
        plt.title('Best Price')
        plt.xlabel('Events')
        plt.ylabel('Price')
        plt.legend(['Best Ask', 'Best Bid'])

        plt.subplot(221)
        plt.bar(bid_prices, bid_volumes, width=0.01, color='b', align='edge')
        plt.xlabel('Price')
        plt.ylabel('Volume')
        plt.title('Bid Queue')

        plt.subplot(223)
        plt.bar(ask_prices, ask_volumes, width=0.01, color='r', align='edge')
        plt.xlabel('Price')
        plt.ylabel('Volume')
        plt.title('Ask Queue')

        plt.tight_layout()

        plt.show()

        return None

    def plot_vwap(self):
        data = self.order_data

        bid_price_ticks = ['BidPrice1', 'BidPrice2', 'BidPrice3', 'BidPrice4', 'BidPrice5']
        bid_size_ticks = ['BidSize1', 'BidSize2', 'BidSize3', 'BidSize4', 'BidSize5']

        ask_price_ticks = ['AskPrice1', 'AskPrice2', 'AskPrice3', 'AskPrice4', 'AskPrice5']
        ask_size_ticks = ['AskSize1', 'AskSize2', 'AskSize3', 'AskSize4', 'AskSize5']

        events = len(data)

        event_range = np.arange(0, events)

        vwap_bid = list()
        vwap_ask = list()

        for i in range(0, events):
            bid_price = 0.0
            ask_price = 0.0
            bid_vol = 0.0
            ask_vol = 0.0
            row = data.iloc[i]

            for a,b in zip(ask_size_ticks, bid_size_ticks):
                bid_vol += row[b]
                ask_vol += row[a]

            for p,s in zip(bid_price_ticks, bid_size_ticks):
                bid_price += row[p]*row[s]/bid_vol

            for p,s in zip(ask_price_ticks, ask_size_ticks):
                ask_price += row[p]*row[s]/ask_vol

            vwap_bid.append(bid_price)
            vwap_ask.append(ask_price)

        plt.plot(event_range, vwap_bid, color='b')
        plt.plot(event_range, vwap_ask, color='r')
        plt.title('VWAP')
        plt.xlabel('Events')
        plt.ylabel('Price')
        plt.legend(['Bid', 'Ask'])
        plt.show()

        return None
