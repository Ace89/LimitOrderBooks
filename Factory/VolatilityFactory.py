
from Analytics.StandardDeviation import StandardDeviation
from Enums.VolatilityMethod import VolatilityMethod


class VolatilityFactory:

    def __init__(self):
        None

    @staticmethod
    def get_volatility_method(volatilty_type, time_series):

        if volatilty_type == VolatilityMethod.StandardDeviation:
            return StandardDeviation(time_series)

        return None


