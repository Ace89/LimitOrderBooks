
from sklearn import linear_model

from Interfaces.ILinearModel import ILinearModel


class LogisticRegression(ILinearModel, linear_model.LogisticRegression):

    def __init__(self):
        None

    def fit_data(self, x, y):
        return None
