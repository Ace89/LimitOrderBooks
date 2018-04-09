from scipy.stats import norm
from Interfaces.IStatisticalDistribution import IStatisticalDistribution


class GaussianDistribution(IStatisticalDistribution):

    def __init__(self):
        None

    def fit_data(self, time_series):
        return norm.fit(time_series)
