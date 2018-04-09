
from Enums.LinearModel import LinearModel
from Analytics.LinearModel import LinearModel


class LinearModelFactory:

    def __init__(self):
        None

    def get_linear_model(self, linear_model):

        if linear_model == LinearModel.LinearRegression:
            return LinearModel()

        return None
