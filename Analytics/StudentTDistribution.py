
from Analytics.IDistribution import IDistribution
from scipy.stats import t


class StudentTDistribution(IDistribution, t):

    def __init__(self):
        None

    def fit_data(self, time_series):
        return t.fit(time_series)
