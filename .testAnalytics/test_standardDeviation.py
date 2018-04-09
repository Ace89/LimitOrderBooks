
from unittest import TestCase
import datetime
import numpy as np
from Enums.DataType import DataType
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Data.TimeSeriesRepository import TimeSeriesRepository
from Time.TimeStructure import TimeStructure
from Analytics.SummaryStatistics import SummaryStatistics
from Analytics.StandardDeviation import StandardDeviation


class TestStandardDeviation(TestCase):
    def test_calculate_volatility(self):
        # arrange
        file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
        ticker = 'AMZN'
        start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
        end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
        date = datetime.datetime(year=2012, month=6, day=21)
        timeSeriesRepository = TimeSeriesRepository(file_path)
        timeStructure = TimeStructure(start_date, end_date)
        timeStructure.create_time_structure(intervals=300)
        timeSeriesRepository.create_time_bucket_structure(timeStructure, ticker, date, DataType.message, 5,
                                                          OrderType.Visible_Execution, OrderDirection.Buy)
        time_structure_sell = TimeStructure(start_date, end_date)
        time_structure_sell.create_time_structure(intervals=300)
        timeSeriesRepository.create_time_bucket_structure(time_structure_sell, ticker, date, DataType.message, 5,
                                                            OrderType.Visible_Execution, OrderDirection.Sell)

        book_imbalance = []
        for i in range(0, len(time_structure_sell.time_structure)):
            book_imbalance.append(time_structure_sell.time_structure[i].sell_orders / timeStructure.time_structure[i].buy_orders)

        summary_statistics = SummaryStatistics(timeStructure)

        # act
        standard_deviation = StandardDeviation(summary_statistics.time_series)
        vol = standard_deviation.calculate_volatility()

        mean = np.average(summary_statistics.time_series)
        temp_vol = 0.0

        for val in summary_statistics.time_series:
            temp_vol += (val - mean)**2

        expected_result = np.sqrt(temp_vol / (len(summary_statistics.time_series)-1))

        # assert
        self.assertTrue(expected_result, vol)
