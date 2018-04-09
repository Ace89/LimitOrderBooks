from unittest import TestCase


class TestTimeSeriesRepository(TestCase):
    def test__convert_datetime_to_seconds(self):
        # arrange
        import datetime
        from Data.TimeSeriesRepository import TimeSeriesRepository
        time_series_repository = TimeSeriesRepository('')
        date_time = datetime.datetime(year=2018, month=3, day=10, hour=9, minute=30)
        result = 34200

        # act
        seconds = time_series_repository._convert_datetime_to_seconds(date_time)

        # assert
        self.assertTrue(seconds == result)

    def test__create_file_name(self):
        # arrange
        import datetime
        from Data.TimeSeriesRepository import TimeSeriesRepository
        from Enums.DataType import DataType
        time_series_repository = TimeSeriesRepository('')
        date_time = datetime.datetime(year=2012, month=6, day=21)
        ticker = 'AMZN'
        time = 5
        result = 'AMZN_2012-06-21_34200000_57600000_message_5.csv'

        # act
        file_path = time_series_repository._create_file_name(ticker, date_time, DataType.message, time)

        # assert
        self.assertTrue(file_path == result)

    def test__filter_data_matrix(self):
        # arrange
        import datetime
        from Data.TimeSeriesRepository import TimeSeriesRepository
        from Enums.OrderType import OrderType
        from Enums.OrderDirection import OrderDirection
        from Enums.DataType import DataType
        file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
        ticker = 'AMZN'
        date = datetime.datetime(year=2012, month=6, day=21)
        time_series_repository = TimeSeriesRepository(file_path)
        time_stamp = 5
        classifier = DataType.message
        order_type = OrderType.Visible_Execution
        order_direction = OrderDirection.Buy
        data = time_series_repository.get_data(ticker, date, classifier, time_stamp).as_matrix()
        data_flag = True
        order_type_vals = (data[:, 1] == order_type.value)
        order_direction_vals = (data[:, 5] == order_direction.value)

        # act
        filtered_data = time_series_repository._filter_data_matrix(data, order_type_vals, order_direction_vals)
        rows, cols = filtered_data.shape

        for i in range(0, rows):
            if filtered_data[i, 1] != order_type.value or filtered_data[i, 5] != order_direction.value:
                data_flag = False

        # assert
        self.assertTrue(data_flag)

    def test_get_data(self):
        # arrange
        import datetime
        from Data.TimeSeriesRepository import TimeSeriesRepository
        from Enums.DataType import DataType
        file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
        ticker = 'AMZN'
        date = datetime.datetime(year=2012, month=6, day=21)
        time_series_repository = TimeSeriesRepository(file_path)
        time_stamp = 5
        classifier = DataType.message

        # act
        data = time_series_repository.get_data(ticker, date, classifier, time_stamp).as_matrix()

        # assert
        self.assertTrue(data is not None)

    def test_create_time_bucket_structure(self):
        # arrange
        import datetime
        from Data.TimeSeriesRepository import TimeSeriesRepository
        from Time.TimeStructure import TimeStructure
        from Enums.OrderType import OrderType
        from Enums.OrderDirection import OrderDirection
        from Enums.DataType import DataType
        file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
        ticker = 'AMZN'
        start_date = datetime.datetime(year=2012, month=6, day=21, hour=9, minute=30)
        end_date = datetime.datetime(year=2012, month=6, day=21, hour=16)
        date = datetime.datetime(year=2012, month=6, day=21)
        timeSeriesRepository = TimeSeriesRepository(file_path)
        timeStructure = TimeStructure(start_date, end_date)
        timeStructure.create_time_structure(intervals=300)

        # act
        timeSeriesRepository.create_time_bucket_structure(timeStructure, ticker, date, DataType.message, 5,
                                                          OrderType.Visible_Execution, OrderDirection.Buy)
        # assert
        self.assertTrue(timeStructure.time_structure is not None)
