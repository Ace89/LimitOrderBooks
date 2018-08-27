
class SummaryStatisticsResult:

    def __init__(self,
                 start_time,
                 end_time,
                 num_buy_orders,
                 num_sell_orders,
                 num_delete_buy_orders,
                 num_delete_sell_orders,
                 num_trades,
                 num_buy_trades,
                 num_sell_trades,
                 avg_price_buy_orders,
                 avg_price_sell_orders,
                 avg_price_deleted_buy_orders,
                 avg_price_deleted_sell_orders,
                 avg_trade_price,
                 std_price_buy_orders,
                 std_price_sell_orders,
                 std_price_deleted_buy_orders,
                 std_price_deleted_sell_orders,
                 std_trade_price,
                 med_price_buy_orders,
                 med_price_sell_orders,
                 med_price_deleted_buy_orders,
                 med_price_deleted_sell_orders,
                 med_trade_price,
                 avg_size_buy_orders,
                 avg_size_sell_orders,
                 avg_size_deleted_buy_orders,
                 avg_size_deleted_sell_orders,
                 avg_size_price,
                 std_size_buy_orders,
                 std_size_sell_orders,
                 std_size_deleted_buy_orders,
                 std_size_deleted_sell_orders,
                 std_size_price,
                 med_size_buy_orders,
                 med_size_sell_orders,
                 med_size_deleted_buy_orders,
                 med_size_deleted_sell_orders,
                 med_trade_size
                 ):
        self.start_time = start_time
        self.end_time = end_time
        self.num_buy_orders = num_buy_orders
        self.num_sell_orders = num_sell_orders
        self.num_delete_buy_orders = num_delete_buy_orders
        self.num_delete_sell_orders = num_delete_sell_orders
        self.num_trades = num_trades
        self.num_buy_trades = num_buy_trades
        self.num_sell_trades = num_sell_trades
        self.avg_price_buy_orders = avg_price_buy_orders
        self.avg_price_sell_orders = avg_price_sell_orders
        self.avg_price_deleted_buy_orders = avg_price_deleted_buy_orders
        self.avg_price_deleted_sell_orders = avg_price_deleted_sell_orders
        self.avg_trade_price = avg_trade_price
        self.std_price_buy_orders = std_price_buy_orders
        self.std_price_sell_orders = std_price_sell_orders
        self.std_price_deleted_buy_orders = std_price_deleted_buy_orders
        self.std_price_deleted_sell_orders = std_price_deleted_sell_orders
        self.std_trade_price = std_trade_price
        self.med_price_buy_orders = med_price_buy_orders
        self.med_price_sell_orders = med_price_sell_orders
        self.med_price_deleted_buy_orders = med_price_deleted_buy_orders
        self.med_price_deleted_sell_orders = med_price_deleted_sell_orders
        self.med_trade_price = med_trade_price
        self.avg_size_buy_orders = avg_size_buy_orders
        self.avg_size_sell_orders = avg_size_sell_orders
        self.avg_size_deleted_buy_orders = avg_size_deleted_buy_orders
        self.avg_size_deleted_sell_orders = avg_size_deleted_sell_orders
        self.avg_size_price = avg_size_price
        self.std_size_buy_orders = std_size_buy_orders
        self.std_size_sell_orders = std_size_sell_orders
        self.std_size_deleted_buy_orders = std_size_deleted_buy_orders
        self.std_size_deleted_sell_orders = std_size_deleted_sell_orders
        self.std_size_price = std_size_price
        self.med_size_buy_orders = med_size_buy_orders
        self.med_size_sell_orders = med_size_sell_orders
        self.med_size_deleted_buy_orders = med_size_deleted_buy_orders
        self.med_size_deleted_sell_orders = med_size_deleted_sell_orders
        self.med_trade_size = med_trade_size
