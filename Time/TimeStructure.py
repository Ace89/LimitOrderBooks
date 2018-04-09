
import datetime
from Time.Bucket import Bucket

"""
Create a time structure of buckets over a specified interval
"""


class TimeStructure:

    def __init__(self, start_time, end_time):
        """
        :param start_time: start time
        :param end_time: end time
        """
        if type(start_time) != datetime.datetime:
            raise Exception("Start time must be of type datetime.time")

        if type(end_time) != datetime.datetime:
            raise Exception("End time must be of type datetime.time")

        self.start_time = start_time
        self.end_time = end_time
        self.time_structure = list()
        self.intervals = None

    def create_time_structure(self, intervals):
        """
        :param intervals: specify intervals in terms of seconds
        :return: None, populates instance list time_structure
        """

        interval = datetime.timedelta(seconds=intervals)
        self.intervals = interval
        temp = self.start_time

        while temp < self.end_time:
            bucket = Bucket(temp, temp+interval)
            self.time_structure.append(bucket)
            temp += interval

if __name__ == '__main__':
    _start_time = datetime.datetime(2018, 1, 30, hour=9, minute=30)
    _end_time = datetime.datetime(2018, 1, 30, hour=16)
    timeStructure = TimeStructure(_start_time, _end_time)
    timeStructure.create_time_structure(300)
    print('Structure created')