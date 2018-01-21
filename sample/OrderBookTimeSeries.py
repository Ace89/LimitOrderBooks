
import numpy as np
from sample.TimeBuckets import TimeBuckets


class OrderBookTimeSeries:

    def __init__(self, time_bucket):
        self.time_bucket = time_bucket

    def get_average_value_time_series(self, buy_or_sell, price_or_volume):
        #buckets are lists of lists
        [buy_buckets, sell_buckets] = self.time_bucket.create_order_book_average_buckets()
        output = []

        if buy_or_sell == 'buy':
            if price_or_volume == 'price':
                for i in range(0,len(buy_buckets)):
                    output.append(buy_buckets[i][0])
            else:
                for i in range(0,len(buy_buckets)):
                    output.append(buy_buckets[i][1])
        else:
            if price_or_volume == 'price':
                for i in range(0,len(sell_buckets)):
                    output.append(sell_buckets[i][0])
            else:
                for i in range(0,len(sell_buckets)):
                    output.append(sell_buckets[i][1])

        return output

    def get_order_book_time_series(self, buy_or_sell, price_or_volume, book_level, order_level):
        tree_buckets = self.time_bucket.create_order_book_tree_buckets(book_level)
        output = []

        if buy_or_sell == 'buy':
            if price_or_volume == 'price':
                for i in range(0, len(tree_buckets)):
                    buy_level = tree_buckets[i].buy_levels# dictionary
                    count =0
                    for key in buy_level:
                        if count == order_level:
                            output.append(key)
                        count += 1
            else:
                for i in range(0, len(tree_buckets)):
                    buy_level = tree_buckets[i].buy_levels# dictionary
                    count =0
                    for key in buy_level:
                        if count == order_level:
                            output.append(np.sum(buy_level[key]))
                        count += 1
        else:
            if price_or_volume == 'price':
                for i in range(0, len(tree_buckets)):
                    sell_level = tree_buckets[i].sell_levels# dictionary
                    count = 0
                    for key in sell_level:
                        if count == order_level:
                            output.append(key)
                        count += 1
            else:
                for i in range(0, len(tree_buckets)):
                    sell_level = tree_buckets[i].sell_levels# dictionary
                    count = 0
                    for key in sell_level:
                        if count == order_level:
                            output.append(np.sum(sell_level[key]))# volumes can be lists so sum to get cumulative
                        count += 1

        return output
