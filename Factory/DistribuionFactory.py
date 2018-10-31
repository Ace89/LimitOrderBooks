
from Analytics.IStatisticalTest import IStatisticalTest


class StatisticalTestFactory:

    def get_statistical_test(self, test_name):

        if test_name == 'student-t':
            return StudentTDistribution()
        else:
            raise NotImplementedError('Distribution not supported')
