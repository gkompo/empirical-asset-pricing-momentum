import statsmodels.api as sm
import pandas as pd

def capm(stock_ret, market_ret):
    X = sm.add_constant(market_ret)
    return sm.OLS(stock_ret, X, missing='drop').fit()

def fama_french_5(stock_ret, ff5):
    X = sm.add_constant(ff5[['MKT_RF','SMB','HML','RMW','CMA']])
    return sm.OLS(stock_ret, X, missing='drop').fit()