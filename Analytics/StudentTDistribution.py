from scipy.stats import t
from Interfaces.IStatisticalDistribution import IStatisticalDistribution


class StudentTDistribution(IStatisticalDistribution):

    def __init__(self):
        None

    def fit_data(self, time_series):
        return t.fit(time_series)
