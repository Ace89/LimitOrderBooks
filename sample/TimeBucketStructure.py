
import numpy as np
import datetime
from sample.TimeBucket import TimeBucket


# start from 34,200 till 57,600
class TimeBucketStructure:

    def __init__(self, date, start_time, end_time, intervals):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.intervals = intervals
        None

    def create_structure(self):

        None

    @staticmethod
    def _convert_seconds_to_time(time_seconds):
        seconds_in_hour = 3600
        seconds_in_min = 60
        time = time_seconds / seconds_in_hour
        hours = np.floor(time)
        mins = np.floor((time - hours)*seconds_in_min)
        secs = np.floor(((time - hours)*seconds_in_min - mins)*seconds_in_min)
        micro = (((time - hours)*seconds_in_min - mins)*seconds_in_min - secs)*1000000
        result = datetime.time(hour=int(hours), minute=int(mins), second=int(secs), microsecond=int(np.floor(micro)))
        #result =  datetime.time()
        return result


if __name__ == '__main__':
    timeBucketStructure = TimeBucketStructure(5, 5, 5, 5)
    temp = timeBucketStructure._convert_seconds_to_time(34218)
    print("hours:" + str(temp.hour))
    print("minute:" + str(temp.minute))
    print("seconds:" + str(temp.second))
    print("microseconds:" + str(temp.microsecond))