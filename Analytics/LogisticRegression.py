
from Analytics.ILinearModel import ILinearModel
from sklearn import linear_model


class LogisticRegression(ILinearModel, linear_model.LogisticRegression):

    def __init__(self):
        None

    def fit_data(self, x, y):
        return None
