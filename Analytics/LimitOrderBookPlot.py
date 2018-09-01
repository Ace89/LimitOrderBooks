
import matplotlib.pyplot


class LimitOrderBookPlot(matplotlib.pyplot):

    def __init__(self, time_series_factory, start_time, time_interval):
        self.time_series_factory = time_series_factory
        self.start_time = start_time
        self.time_interval = time_interval

    def plot_sizes(self, attribute, time_series_type):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        # use the time series factory to create the time series and plot
        raise NotImplementedError('Not implemented yet')

    def plot_price(self, attribute, time_series_type):
        """
        :param attribute: size or price
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        # use the time series factory to create the time series and plot
        raise NotImplementedError('Not implemented yet')

    def animation(self, attribute, time_series_type):
        """
        :param attribute:
        :param time_series_type: see TimeSeriesTypes
        :return:
        """
        # use the time series factory to create the time series and plot
        raise NotImplementedError('Not implemented yet')