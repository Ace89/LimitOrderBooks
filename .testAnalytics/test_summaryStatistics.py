
from unittest import TestCase
import datetime
import numpy as np
from Enums.DataType import DataType
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Data.TimeSeriesRepository import TimeSeriesRepository
from Time.TimeStructure import TimeStructure
from Analytics.SummaryStatistics import SummaryStatistics


class TestSummaryStatistics(TestCase):
    @staticmethod
    def create_time_structure(order_type_execution, order_direction):
        file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
        ticker = 'AMZN'
        start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
        end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
        date = datetime.datetime(year=2012, month=6, day=21)
        timeSeriesRepository = TimeSeriesRepository(file_path)
        timeStructure = TimeStructure(start_date, end_date)
        timeStructure.create_time_structure(intervals=300)
        timeSeriesRepository.create_time_bucket_structure(timeStructure, ticker, date, DataType.message, 5,
                                                          order_type_execution, order_direction)
        return timeStructure

    def test_create_array(self):
        # arrange
        time_structure = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Buy)
        summary_statistics = SummaryStatistics(time_structure)
        time_series = summary_statistics.create_array()

        flag = True

        # act
        for i in range(0, len(time_series)):
            if time_structure.time_structure[i].price != time_series[i]:
                flag = False

        # assert
        self.assertTrue(flag)

    def test_calculate_mean(self):
        # arrange
        time_structure = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Buy)
        summary_statistics = SummaryStatistics(time_structure)
        time_series = summary_statistics.create_array()

        temp_prices = 0.0

        # act
        for val in time_series:
            temp_prices += val

        expected_result = temp_prices / len(time_series)

        # assert
        self.assertTrue(expected_result, summary_statistics.calculate_mean())

    def test_calculate_median(self):
        # arrange
        time_structure = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Buy)
        summary_statistics = SummaryStatistics(time_structure)
        time_series = summary_statistics.create_array()

        # act
        expected_result = np.median(time_series)

        # assert
        self.assertTrue(expected_result, summary_statistics.calculate_median())

    def test_calculate_percentile(self):
        # arrange
        time_structure = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Buy)
        summary_statistics = SummaryStatistics(time_structure)
        time_series = summary_statistics.create_array()
        pctile = 10

        # act
        expected_result = np.percentile(time_series, pctile)

        # assert
        self.assertTrue(expected_result, summary_statistics.calculate_percentile(pctile))

    def test_calculate_imbalance(self):
        # arrange
        time_structure_buy = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Buy)
        time_structure_sell = self.create_time_structure(OrderType.Visible_Execution, OrderDirection.Sell)
        summary_statistics = SummaryStatistics(time_structure_buy)
        expected_result = 96.9142684586
        tol = 10e-3

        # act
        imbalance = summary_statistics.calculate_book_imbalance(time_structure_buy.time_structure, time_structure_sell.time_structure)
        sum_imbalance = np.sum(imbalance)

        # assert
        self.assertTrue(np.abs(expected_result - sum_imbalance) < tol)
