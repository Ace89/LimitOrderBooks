
from sklearn import linear_model


class LinearModel:

    def __int__(self):
        None

    def fit_data(self, time_series_x, time_series_y):
        regr = linear_model.LinearRegression()
        regr.fit(time_series_x, time_series_y)
        return [regr.intercept_, regr.coef_]