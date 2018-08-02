
if __name__ == '__main__':
    import time
    import matplotlib.pyplot as plt
    import numpy as np

    from Analytics.LimitOrderBook.LimitOrderBook import LimitOrderBook
    from Analytics.LimitOrderBook.MessageDataReader import MessageDataReader
    from Analytics.LimitOrderBook.LimitOrderBookUpdater import LimitOrderBookUpdater

    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = 'AMZN_2012-06-21_34200000_57600000_message_5_subset.csv'

    lob = LimitOrderBook()
    msgDataReader = MessageDataReader()
    lob_updater = LimitOrderBookUpdater()

    start = time.time()

    msgDataReader.read_messages(file_path+file_name)
    lob_updater.update_order_book(lob, msgDataReader.messages)

    bid_price, bid_volume, ask_price, ask_volume = lob_updater.create_time_series()

    bid = np.asarray(bid_price)
    ask = np.asarray(ask_price)

    plt.subplot(2, 1, 1)
    plt.plot(bid/10000)
    plt.title('Bid')

    plt.subplot(2, 1, 2)
    plt.plot(ask/10000)
    plt.title('Ask')

    plt.show()

    end = time.time()

