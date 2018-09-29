
from scipy.stats import t

from Interfaces.IDistribution import IDistribution


class StudentTDistribution(IDistribution):

    def __init__(self):
        None

    def fit_data(self, time_series):
        return t.fit(time_series)
