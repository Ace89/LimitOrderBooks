
class DataReaderResult:

    def __init__(self, time, bid_queue, ask_queue):
        """
        :param time: Time
        :param bid_queue: Bid queue
        :param ask_queue: Ask queue
        """
        self.time = time
        self.bid_queue = bid_queue
        self.ask_queue = ask_queue
