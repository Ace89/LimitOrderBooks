
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.api import VAR, DynamicVAR
from statsmodels.tsa.base.datetools import dates_from_str
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # load real gdp, consumption and investment data
    # mdata => macro data
    mdata = sm.datasets.macrodata.load_pandas().data
    # year and quarter are separate columns, aim is to combine them into one
    dates = mdata[['year', 'quarter']].astype(int).astype(str)
    quarterly = dates["year"] + "Q" + dates["quarter"]

    quarterly = dates_from_str(quarterly)
    # create a pandas dataframe, with dates as index
    mdata = mdata[['realgdp', 'realcons', 'realinv']]
    mdata.index = pd.DatetimeIndex(quarterly)

    # take daily log differences of data and remove any na values
    data = np.log(mdata).diff().dropna()

    # initialize VAR model
    model = VAR(data)
    # fit VAR model to data, specify lag
    results = model.fit(2)

    #plt.plot(np.log(mdata['realgdp']).diff().dropna())
    #plt.show()

    #model.select_order(15)

    lag_order = results.k_ar
    #print(results.forecast(data.values[-lag_order:],5))

    results.plot_forecast(10)

    #print(results.summary())

