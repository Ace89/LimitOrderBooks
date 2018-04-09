
import numpy as np
from datetime import datetime


class TimeBucket:

    def __init__(self, time_start, time_end):
        """
        :param time_start: start time of bucket
        :param time_end: end time of bucket
        """
        self.time_start = time_start
        self.time_end = time_end
