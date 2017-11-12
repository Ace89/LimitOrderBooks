"""

    Bucket is for time bucket class,
    it will hold data for each time bucket
    intended to be a data container
"""


class Bucket:

    def __init__(self, time_start, time_end, ask_price, bid_price,ask_freq,bid_freq):
        self.time_start = time_start
        self.time_end = time_end
        self.best_ask_price = ask_price
        self.best_bid_price = bid_price
        self.ask_volume_levels = {}  # keys to these dictionaries will be "level 1", "level 2" ... etc
        self.bid_volume_levels = {}
        self.ask_frequency = ask_freq
        self.buy_frequency = bid_freq

    def init_volume_levels(self, levels):

        for i in (0, levels):
            key = "level" + str(i)
            self.ask_volume_levels[key] = 0
            self.bid_volume_levels[key] = 0
