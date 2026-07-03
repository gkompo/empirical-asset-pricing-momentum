import statsmodels.api as sm
import pandas as pd

def capm(stock_ret, mkt_rf):
    X = sm.add_constant(mkt_rf)
    return sm.OLS(stock_ret, X).fit()


def fama_french_5(stock_ret, ff5):
    X = sm.add_constant(ff5[['MKT_RF','SMB','HML','RMW','CMA']])
    return sm.OLS(stock_ret, X).fit()