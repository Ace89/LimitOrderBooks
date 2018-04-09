from Enums.DistributionMethod import DistributionMethod
from Analytics.GaussianDistribution import GaussianDistribution
from Analytics.StudentTDistribution import StudentTDistribution


class DistributionFactory:

    def __init__(self):
        None

    def get_distribution(self, distribution_method):

        if distribution_method == DistributionMethod.Gaussian:
            return GaussianDistribution()
        elif distribution_method == DistributionMethod.StudentT:
            return StudentTDistribution()

        return None
