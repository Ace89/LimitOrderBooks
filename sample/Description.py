
"""
Aim
-> This class will be used to produce descriptions and plots of time buckets

"""

import numpy as np
from sample.PriceLevel import PriceLevel
import matplotlib.pyplot as plt

__author__ = 'Awais Talib'
__project__ = 'Limit Order Books'
__maintainer__ = ''
__license__ = ''
__version__ = '0.1'
__all__ = ''


class Description:

    @staticmethod
    def __doc__():
        return 'To display summary stats and plots given time buckets'

    def __init__(self, time_buckets):
        pass

    def sort_price_levels(self, price_levels):
        # get an infinite loop here
        changes = 1
        while changes > 0:
            changes = 0
            for i in range(1, len(price_levels)):
                if price_levels[i-1] > price_levels[i]:
                    changes += 1
                    a = price_levels[i]
                    b = price_levels[i-1]
                    price_levels[i-1] = a
                    price_levels[i] = b

        return None

    def short_summary(self):
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows - 1, 0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor) * 60.0
        bids = 0
        offers = 0

        for i in range(0, rows):
            if self.current_matrix[i, 1] == 1:
                if self.current_matrix[i, 5] == 1:
                    bids += 1
                else:
                    offers += 1

        print('\nCurrent order book time: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))
        print('Message Index: {0:5d}'.format(rows))
        print('Bid Orders: {0:5d}'.format(bids))
        print('Ask Orders: {0:5d}'.format(offers))
        print('Total Orders: {0:5d}'.format(bids + offers))
        None

    def summary(self):
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows - 1, 0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor) * 60.0
        bids = 0
        offers = 0

        for i in range(0, rows):
            if self.current_matrix[i, 1] == 1:
                if self.current_matrix[i, 5] == 1:
                    bids += 1
                else:
                    offers += 1

        print('\nCurrent order book time: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))
        print('Message Index: {0:5d}'.format(rows))
        print('Bid Orders: {0:5d}'.format(bids))
        print('Ask Orders: {0:5d}'.format(offers))
        print('Total Orders: {0:5d}'.format(bids + offers))
        None

    def display(self):
        # plot diagram of two stacks, buy and sell stack
        # https://matplotlib.org/examples/pylab_examples/subplots_demo.html
        [bid_levels, offer_levels] = self._sort_price_levels()
        print("Number of bid levels: " + str(len(bid_levels)))
        width = 0.05
        ind = np.arange(1)
        scale = 10000
        mid_price = (bid_levels[0].get_price() + offer_levels[0].get_price()) * 0.5
        mid_price = mid_price / scale

        bids = (bid_levels[0].get_price() / scale, bid_levels[1].get_price() / scale, bid_levels[2].get_price() / scale,
                bid_levels[3].get_price() / scale, bid_levels[4].get_price() / scale)

        offers = (
        offer_levels[0].get_price() / scale, offer_levels[1].get_price() / scale, offer_levels[2].get_price() / scale,
        offer_levels[3].get_price() / scale, offer_levels[4].get_price() / scale)

        offer_level_0 = offer_levels[0].get_price()
        offer_level_0 = offer_level_0 / scale
        offer_level_1 = offer_levels[1].get_price() - offer_levels[0].get_price()
        offer_level_1 = offer_level_1 / scale
        offer_level_2 = offer_levels[2].get_price() - offer_levels[1].get_price()
        offer_level_2 = offer_level_2 / scale
        offer_level_3 = offer_levels[3].get_price() - offer_levels[2].get_price()
        offer_level_3 = offer_level_3 / scale
        offer_level_4 = offer_levels[4].get_price() - offer_levels[3].get_price()
        offer_level_4 = offer_level_4 / scale

        bid_level_0 = bid_levels[0].get_price()
        bid_level_0 = bid_level_0 / scale
        bid_level_1 = bid_levels[1].get_price() - bid_levels[0].get_price()
        bid_level_1 = bid_level_1 / scale
        bid_level_2 = bid_levels[2].get_price() - bid_levels[1].get_price()
        bid_level_2 = bid_level_2 / scale
        bid_level_3 = bid_levels[3].get_price() - bid_levels[2].get_price()
        bid_level_3 = bid_level_3 / scale
        bid_level_4 = bid_levels[4].get_price() - bid_levels[3].get_price()
        bid_level_4 = bid_level_4 / scale

        p1 = plt.bar(ind, bid_level_0, width, color='b')
        p2 = plt.bar(ind, bid_level_1, width, bottom=bid_level_0, color='r')
        p3 = plt.bar(ind, bid_level_2, width, bottom=bid_level_1, color='b')
        p4 = plt.bar(ind, bid_level_3, width, bottom=bid_level_2, color='r')
        p5 = plt.bar(ind, bid_level_4, width, bottom=bid_level_3, color='b')
        p6 = plt.bar(ind, offer_level_0, width, bottom=bid_level_4, color='r')
        p7 = plt.bar(ind, offer_level_1, width, bottom=offer_level_0, color='b')
        p8 = plt.bar(ind, offer_level_2, width, bottom=offer_level_1, color='r')
        p9 = plt.bar(ind, offer_level_3, width, bottom=offer_level_2, color='b')
        p10 = plt.bar(ind, offer_level_4, width, bottom=offer_level_3, color='r')

        plt.ylabel('Prices')
        plt.title('Bid Offer prices')
        # plt.xticks(ind,('Levels'))
        plt.yticks(np.arange(bid_level_0 - 0.01, offer_level_4 + 0.01, 0.01))
        plt.tight_layout()
        plt.show()

        """
        f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
        ax1.set_title('Limit Order Book')
        ax1.bar(ind + width + width, offers, width, color='r')
        ax2.bar(ind, bids, width, color='b')
        f.subplots_adjust(hspace=0)

        plt.tight_layout()
        plt.show()

        plt.ylabel('Prices')
        plt.title('Bid Offer prices')
        plt.xticks(ind, ('Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5'))
        plt.legend((p1[0], p2[0]), ('bid', 'offer'))
        plt.show()

        for i in range(0, 5):
            print('{0} --- {1}'.format(bid_levels[i].get_price(), bid_levels[i].get_volumes()[0]))

        print('---------------------------------------------------')

        for i in range(0, 5):
            print('{0} --- {1}'.format(offer_levels[i].get_price(), offer_levels[i].get_volumes()[0]))
        """
        None

    def book_imbalance(self):
        # This should be in Time Buckets
        # ratio of bid and ask orders
        # use just orders in level 1
        return 0.0

    def _sort_price_levels(self): # private method
        rows, cols = np.shape(self.current_matrix)
        current_book_time = self.current_matrix[rows - 1, 0] / self.seconds_in_hour
        time_floor = np.floor(current_book_time)
        mins = (current_book_time - time_floor) * 60.0

        bid_price_range = []
        offer_price_range = []
        for i in range(0, rows):
            if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 5] == 1:
                bid_price_range.append(self.current_matrix[i, 4])
            elif self.current_matrix[i, 1] == 1 and self.current_matrix[i, 5] == -1:
                offer_price_range.append(self.current_matrix[i, 4])
        bid_price_range = np.array(bid_price_range)
        bid_price_range = np.unique(bid_price_range)
        offer_price_range = np.array(offer_price_range)
        offer_price_range = np.unique(offer_price_range)

        bid_levels = []  # contains price level objects
        offer_levels = []  # contains price level objects
        # differentiate between bid and ask price levels
        for val in bid_price_range:
            # create a price level object
            bid_price_level = PriceLevel(val)
            for i in range(0, rows):
                if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 4] == val and self.current_matrix[i, 5] == 1:
                    bid_price_level.add_volume(self.current_matrix[i, 3])
            bid_levels.append(bid_price_level)

        for val in offer_price_range:
            # create a price level object
            offer_price_level = PriceLevel(val)
            for i in range(0, rows):
                if self.current_matrix[i, 1] == 1 and self.current_matrix[i, 4] == val and self.current_matrix[i, 5] == -1:
                    offer_price_level.add_volume(self.current_matrix[i, 3])
            offer_levels.append(offer_price_level)

        print('Current time is: ' + str(int(time_floor)) + ':' + str(np.round(mins, 0)))

        self.sort_price_levels(bid_levels)
        self.sort_price_levels(offer_levels)
        return [bid_levels, offer_levels]

    def plot(self):
        pass

    def supply_demand(self):
        # normalize price levels using the absolute difference between best ask and mid price
        # normalize volume levels using sum of sizes across all plotted price levels on each side
        # first calculate mid price, then best ask price

        [bid_levels, offer_levels] = self._sort_price_levels()

        mid_price = (offer_levels[0].get_price() + bid_levels[-1].get_price()) * 0.50

        ask_price_normalize = np.abs(offer_levels[-1].get_price() - mid_price)
        bid_price_normalize = np.abs(bid_levels[-1].get_price() - mid_price)

        ask_price = []
        bid_price = []

        ask_volume_normalize = 0.0
        bid_volume_normalize = 0.0

        ask_volume = []
        bid_volume = []

        size = len(offer_levels)

        if size != len(bid_levels):
            print("bids and offers not same size")

        for i in range(0, size):
            ask_price.append(offer_levels[i].get_price() / ask_price_normalize)
            ask_volume_normalize += np.sum(offer_levels[i].get_volumes())
            bid_price.append(bid_levels[i].get_price() / bid_price_normalize)
            bid_volume_normalize += np.sum(bid_levels[i].get_volumes())

        for i in range(0, size):
            ask_volume.append(np.sum(offer_levels[i].get_volumes())/ask_volume_normalize)
            bid_volume.append(np.sum(bid_levels[i].get_volumes())/bid_volume_normalize)

        self.sort_price_levels(ask_volume)
        self.sort_price_levels(ask_price)
        self.sort_price_levels(bid_volume)
        self.sort_price_levels(bid_price)

        # do a sub plot here
        # last value in bid_levels is the best bid price
        # first value in offer levels is the best ask price
        # average of the two is the mid

        plt.subplot(2, 1, 1)
        plt.plot(ask_volume, ask_price)
        plt.title('Ask volumes')
        plt.ylabel('Price')

        plt.subplot(2, 1, 2)
        plt.plot(bid_volume, bid_price)
        plt.title('Bid volumes')
        plt.ylabel('Price')

        plt.show()

        return None
